from django.urls import reverse
from datetime import timedelta,datetime
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
# from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from itertools import chain
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse, response
from django.views import View
import json
import requests
from django.contrib.auth.models import User
from a_system.models import OurInterFriends
from a_webinar.models import *
from api.serializers import *
import jwt
# send email
import random
from django.core.mail import EmailMultiAlternatives
from qaamuus_acd import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from qaamuus_acd import settings
# Create your views here.
# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_url={
        'Doc-List':'/doc-list/',
        'Doc-create':'doc-create/',
        'Delete':'',
    }
    return Response(api_url)



# user 
@api_view(['GET'])
def userList(request):
    user=User.objects.all()
    serializer=UserSerializer(user,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def userCreate(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        theUser=User.objects.get(pk=serializer.data['id'])
        theUser.set_password(theUser.password)
        theUser.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

def passwordFormat(request,pk):
    theUser=User.objects.get(pk=pk)
    theUser.set_password(theUser.password)
    theUser.save()
    return HttpResponse(theUser)
@api_view(['POST'])
def userUpdate(request,pk):
    user=User.objects.get(pk=pk)
    serializer=UserSerializer(instance=user,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        theUser=User.objects.get(pk=serializer.data['id'])
        theUser.set_password(theUser.password)
        theUser.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def userDelete(request,pk):
    theUser=User.objects.get(pk=pk)
    
    theUser.delete()
    return Response()

@api_view(['GET'])
def userDetail(request,pk):
    user=User.objects.get(pk=pk)
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)




@api_view(['GET'])
def jwtAuthTokenUser(request):
    try:
        access_token_obj = AccessToken(str(request.auth))
        theUser=User.objects.get(id=access_token_obj['user_id'])
        userProfileSerializer = UserProfileSerializer(UserProfile.objects.get(user=theUser),many=False)
        return Response(userProfileSerializer.data)
    except:
        access_token_obj = AccessToken(str(request.auth))
        theUser=User.objects.get(id=access_token_obj['user_id'])
        # try:
        #     userProfileSerializer = UserProfileSerializer(UserProfile.objects.get(user=theUser),many=False)
        #     return Response(userProfileSerializer.data)
        # except:
        #     theUserSerializer=UserSerializer(theUser,many=False)
        #     return Response(theUserSerializer.data)
        return Response({'status':404,'message':'token expired please login in again'})


@api_view(['POST'])
def jwtAuthTokenLogin(request):
    theUser=''
    username=request.data['username']
    password=request.data['password']
    if username.find('@')!=-1:
        theUser=User.objects.filter(email=username).first()
    else:
        theUser=User.objects.filter(username=username).first()
    if theUser is None:
        raise AuthenticationFailed('username or email not found')

    if not theUser.check_password(password):
        raise AuthenticationFailed('Incorrect Password')
    
    generatedToken=RefreshToken.for_user(theUser)
    # domain='http://'+str(get_current_site(request).domain)
    # if request.is_secure():
    #     domain = 'https://'+str(get_current_site(request).domain)
    
    
    # response=requests.post(str(domain+'/api/token/'),json={"username":theUser.username,"password":password})
    # tokenResp=json.loads(response.text)
    return Response({"status":200,"refresh":str(generatedToken),"access":str(generatedToken.access_token)})












@api_view(['POST'])
def jwtLogin(request):
    theUser=''
    username=request.data['username']
    password=request.data['password']

    
    if username.find('@')!=-1:
        theUser=User.objects.filter(email=username).first()
    else:
        theUser=User.objects.filter(username=username).first()
    if theUser is None:
        raise AuthenticationFailed('username or email not found')

    if not theUser.check_password(password):
        raise AuthenticationFailed('Incorrect Password')

    payload={
        'id':theUser.id,
        'exp':datetime.utcnow()+timedelta(days=10),
        'iat':datetime.utcnow()
    }
    jwtToken=jwt.encode(payload,'secret',algorithm='HS256')
    
    jwtUserResponse=Response()
    jwtUserResponse.set_cookie(key='jwt',value=jwtToken,httponly=False)

    jwtUserResponse.data={
        'jwt':jwtToken
    }
    return jwtUserResponse

@api_view(['GET'])
def jwtUser(request):
    jwtToken=request.COOKIES.get('jwt')
    if not jwtToken:
        raise AuthenticationFailed("unAuth")
    
    try:
        payload=jwt.decode(jwt=jwtToken,key="secret",algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("unAuthenticated")
    theUser=User.objects.filter(id=payload['id']).first()
    theUserInfo=UserProfile.objects.filter(user=theUser).first()
    serializerUserInfo=UserProfileSerializer(theUserInfo)
    return Response(serializerUserInfo.data)    

@api_view(['GET'])
def jwtLogout(request):
    jwtResponse=Response()
    jwtResponse.delete_cookie('jwt')

    jwtResponse.data={
        "message":"success",
        "code":200
    }      
    return jwtResponse  


@api_view(['GET'])
def checkingUserExist(request,username):
    userr=User.objects.filter(username=username).exists()
    # serializer=ClasseSerializer(classe,many=True)
    return Response({'isExist':userr})
@api_view(['GET'])
def checkingEmailExist(request,email):
    userr=User.objects.filter(email=email).exists()
    # serializer=ClasseSerializer(classe,many=True)
    return Response({'isExist':userr})

@api_view(['GET'])
def checkUserExistEmailAndUsername(request,username,email):
    isExist=True
    if User.objects.filter(username=username).exists()==False and User.objects.filter(email=email).exists()==False:
        isExist=False
    else:
        isExist=True
    
    # serializer=ClasseSerializer(classe,many=True)
    return Response({'isExist':isExist})


def generateRandomReffralCode():
    randomNum ='qReff_'+str(random.randint(4,9000))
    return randomNum



# userprofile
@api_view(['GET'])
def userProfileList(request):
    objects=UserProfile.objects.all()
    serializer=UserProfileSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def userProfileCreate(request):
    userModalData=UserSerializer(data=request.data)
    if userModalData.is_valid():
        userModalData.save()
        theUser=User.objects.get(pk=userModalData.data['id'])
        theUser.set_password(theUser.password)
        theUser.save()
        request.data["user"]=userModalData.data['id']
        request.data["referralCode"]=generateRandomReffralCode()
        userProfileData=UserProfileCreateSerializer(data=request.data)
        if userProfileData.is_valid():
            userProfileData.save()
            return Response({"status": "success", "data": userProfileData.data})
        else:
            return Response({"status": "error", "data": userProfileData.errors})
    else:
        return Response({"status": "error", "data": userModalData.errors})
@api_view(['POST'])
def userProfileUpdate(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    theUser=User.objects.get(pk=(theObject.user).pk)
    userModalData=UserSerializer(instance=theUser,data=request.data,partial=True)
    serializer=UserProfileCreateSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        if userModalData.is_valid():
            userModalData.save()
            try:
                if request.data['password']:
                    theUser.set_password(theUser.password)
                    theUser.save()
            except:
                pass
        else:
            return Response({"status": "error", "data": userModalData.errors})
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def userProfileUpdateEmail(request,email):
    theObject=UserProfile.objects.get(email=email)
    theUser=User.objects.get(pk=(theObject.user).pk)
    userModalData=UserSerializer(instance=theUser,data=request.data,partial=True)
    serializer=UserProfileCreateSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        if userModalData.is_valid():
            userModalData.save()
            try:
                if request.data['password']:
                    theUser.set_password(theUser.password)
                    theUser.save()
            except:
                pass
        else:
            return Response({"status": "error", "data": userModalData.errors})
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def userProfileDelete(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    theObject.user.delete()
    return Response()

@api_view(['GET'])
def userProfileDetail(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    serializer=UserProfileSerializer(theObject,many=False)
    return Response(serializer.data)
@api_view(['GET'])
def userProfileDetailUsername(request,username):
    try:
        theObject=UserProfile.objects.get(user=User.objects.get(username=username))
        serializer=UserProfileSerializer(theObject,many=False)
        return Response(serializer.data)
    except:
        return Response({'status':False,'detail':'invalid username'})

@api_view(['GET'])
def userEnrollmentsDetail(request,pk):
    try:
        theUser=UserProfile.objects.get(pk=pk)
        userReferralCodeBoughts=InrolledCourseSerializer(InrolledCourse.objects.filter(referralCode=theUser.referralCode),many=True)
        enrolledCourses=InrolledCourseSerializer(InrolledCourse.objects.filter(theUser=theUser),many=True)
        bookedEvents=EventEnrolledSerializer(EventEnrolled.objects.filter(theUser=theUser),many=True)
        return Response({'enrolledCourses':enrolledCourses.data,'bookedEvents':bookedEvents.data,'userReferralCodeBoughts':userReferralCodeBoughts.data})
    except:
        return Response({'message':'user not available'})





# qr courses
@api_view(['GET'])
def qaEventList(request):
    objects=EventView.objects.all()
    serializer=EventViewSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def qaEventCreate(request):
    serializer=EventViewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def qaEventUpdate(request,pk):
    theObject=EventView.objects.get(pk=pk)
    serializer=EventViewSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def qaEventDelete(request,pk):
    theObject=EventView.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def qaEventDetail(request,pk):
    theObject=EventView.objects.get(pk=pk)
    serializer=EventViewSerializer(theObject,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def qaEventDetailSlug(request,slug):
    try:
        theObject=EventView.objects.get(slug=slug)
        serializer=EventViewSerializer(theObject,many=False)
        return Response(serializer.data)
    except:
        return Response({'message':'invalid event'})








# qr internation
@api_view(['GET'])
def ourInternationalFriendsList(request):
    objects=OurInterFriends.objects.all()
    serializer=OurInterFriendsSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def ourInternationalFriendsCreate(request):
    serializer=OurInterFriendsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def ourInternationalFriendsUpdate(request,pk):
    theObject=OurInterFriends.objects.get(pk=pk)
    serializer=OurInterFriendsSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def ourInternationalFriendsDelete(request,pk):
    theObject=OurInterFriends.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def ourInternationalFriendsDetail(request,pk):
    theObject=OurInterFriends.objects.get(pk=pk)
    serializer=OurInterFriendsSerializer(theObject,many=False)
    return Response(serializer.data)






# qr feedBacks
@api_view(['GET'])
def feedBacksList(request):
    objects=FeedBacks.objects.all()
    serializer=FeedBacksSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def feedBacksCreate(request):
    serializer=FeedBacksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def feedBacksUpdate(request,pk):
    theObject=FeedBacks.objects.get(pk=pk)
    serializer=FeedBacksSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def feedBacksDelete(request,pk):
    theObject=FeedBacks.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def feedBacksDetail(request,pk):
    theObject=FeedBacks.objects.get(pk=pk)
    serializer=FeedBacksSerializer(theObject,many=False)
    return Response(serializer.data)






# qr courses
@api_view(['GET'])
def qaCoursesList(request):
    objects=QaCourses.objects.all()
    serializer=QaCoursesSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def qaCoursesCreate(request):
    serializer=QaCoursesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def qaCoursesUpdate(request,pk):
    theObject=QaCourses.objects.get(pk=pk)
    serializer=QaCoursesSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def qaCoursesDelete(request,pk):
    theObject=QaCourses.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def qaCoursesDetail(request,pk):
    theObject=QaCourses.objects.get(pk=pk)
    serializer=QaCoursesSerializer(theObject,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def qaCoursesDetailSlug(request,slug):
    theObject=QaCourses.objects.get(slug=slug)
    serializer=QaCoursesSerializer(theObject,many=False)
    
    return Response(serializer.data)









@api_view(['GET'])
def lessonsComponentList(request):
    objects=lessonCompo.objects.all()
    serializer=lessonCompoSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def lessonsComponentCreate(request):
    serializer=lessonCompoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def lessonsComponentUpdate(request,pk):
    theObject=lessonCompo.objects.get(pk=pk)
    serializer=lessonCompoSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def lessonsComponentDelete(request,pk):
    theObject=lessonCompo.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def lessonsComponentDetail(request,pk):
    theObject=lessonCompo.objects.get(pk=pk)
    serializer=lessonCompoSerializer(theObject,many=False)
    return Response(serializer.data)






# qr lessons
@api_view(['GET'])
def lessonList(request):
    objects=Lessons.objects.all().order_by('lessonNum')
    serializer=LessonsSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def thisCourseLessonList(request,pk):
    objects=Lessons.objects.filter(theCourse=QaCourses.objects.get(pk=pk))
    serializer=LessonsSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def lessonCreate(request):
    serializer=LessonsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def lessonUpdate(request,pk):
    theObject=Lessons.objects.get(pk=pk)
    serializer=LessonsSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def lessonDelete(request,pk):
    theObject=Lessons.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def lessonDetail(request,pk):
    theObject=Lessons.objects.get(pk=pk)
    serializer=LessonsSerializer(theObject,many=False)
    return Response(serializer.data)








# qr courses
@api_view(['GET'])
def topicList(request):
    objects=Topic.objects.all()
    serializer=TopicSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def thislessonTopicsList(request,pk):
    objects=Topic.objects.filter(theLesson=Lessons.objects.get(pk=pk))
    serializer=TopicSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def topicCreate(request):
    serializer=TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def topicUpdate(request,pk):
    theObject=Topic.objects.get(pk=pk)
    serializer=TopicSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def topicDelete(request,pk):
    theObject=Topic.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def topicDetail(request,pk):
    theObject=Topic.objects.get(pk=pk)
    serializer=TopicSerializer(theObject,many=False)
    return Response(serializer.data)








# qrCourse reivew
@api_view(['GET'])
def courseReviewList(request):
    objects=CourseReview.objects.all()
    serializer=CourseReviewSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def thisCourseReviewList(request,pk):
    objects=CourseReview.objects.filter(theCourse=QaCourses.objects.get(pk=pk))
    serializer=CourseReviewSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def courseReviewCreate(request):
    serializer=CourseReviewCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def courseReviewUpdate(request,pk):
    theObject=CourseReview.objects.get(pk=pk)
    serializer=CourseReviewCreateSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def courseReviewDelete(request,pk):
    theObject=CourseReview.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def courseReviewDetail(request,pk):
    theObject=CourseReview.objects.get(pk=pk)
    serializer=CourseReviewSerializer(theObject,many=False)
    return Response(serializer.data)










# qrCourses List
@api_view(['GET'])
def discussionList(request):
    objects=LessonDiscussion.objects.all()
    serializer=LessonDiscussionSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def thislessonDiscussionsList(request,pk):
    objects=LessonDiscussion.objects.filter(theLesson=Lessons.objects.get(pk=pk))
    serializer=LessonDiscussionSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def discussionCreate(request):
    serializer=LessonDiscussionCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def discussionUpdate(request,pk):
    theObject=LessonDiscussion.objects.get(pk=pk)
    serializer=LessonDiscussionSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def discussionDelete(request,pk):
    theObject=LessonDiscussion.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def discussionDetail(request,pk):
    theObject=LessonDiscussion.objects.get(pk=pk)
    serializer=LessonDiscussionSerializer(theObject,many=False)
    return Response(serializer.data)



@api_view(['GET'])
def thisUserDiscussionsList(request,userId):
    objects=LessonDiscussion.objects.filter(theUser=UserProfile.objects.get(pk=userId))
    serializer=LessonDiscussionSerializer(objects,many=True)
    return Response(serializer.data)




# notification reivew
@api_view(['GET'])
def userNotificationsList(request):
    objects=UserNotifications.objects.all()
    serializer=UserNotificationsSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def userNotificationsCreate(request):
    serializer=UserNotificationsCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def userNotificationsUpdate(request,pk):
    theObject=UserNotifications.objects.get(pk=pk)
    serializer=UserNotificationsSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})


@api_view(['GET'])
def userNotificationsDetail(request,pk):
    theObject=UserNotifications.objects.get(pk=pk)
    serializer=UserNotificationsSerializer(theObject,many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
def userNotificationsDelete(request,pk):
    theObject=UserNotifications.objects.get(pk=pk)
    theObject.delete()
    return Response()



# notification reivew
@api_view(['GET'])
def thisUserNotificationsList(request,userId):
    try:
        objects=UserNotifications.objects.filter(theUser=UserProfile.objects.get(pk=userId)).order_by('-seen')
        serializer=UserNotificationsSerializer(objects,many=True)
        return Response(serializer.data)
    except:
        return Response({"message":"ivalid id"})




# notification reivew
@api_view(['GET'])
def couponCodeList(request):
    objects=CouponCode.objects.all()
    serializer=CouponCodeSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def couponCodeCreate(request):
    serializer=CouponCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def couponCodeUpdate(request,pk):
    theObject=CouponCode.objects.get(pk=pk)
    serializer=CouponCodeSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})


@api_view(['GET'])
def couponCodeDetail(request,pk):
    theObject=CouponCode.objects.get(pk=pk)
    serializer=CouponCodeSerializer()(theObject,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def couponCodeCheck(request,couponCode):
    try:
        theObject=CouponCode.objects.get(couponCode=couponCode)
        serializer=CouponCodeSerializer(theObject,many=False)
        return Response({'isReferralCode':False,'isCouponCode':True,'isExpired':False,'exists':True,'discountPrice':theObject.discountPrice})
    except:
        theUserReff=UserProfile.objects.filter(referralCode=couponCode)
        if theUserReff.exists():
            return Response({'isReferralCode':True,'isCouponCode':False,'exists':True})
        else:
            return Response({'isReferralCode':False,'isCouponCode':False,'exists':False})

@api_view(['DELETE'])
def couponCodeDelete(request,pk):
    theObject=CouponCode.objects.get(pk=pk)
    theObject.delete()
    return Response()






# notification reivew
@api_view(['GET'])
def voiteModelList(request):
    objects=VoteModel.objects.all()
    serializer=VoiteModelSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def voiteModelCreate(request):
    serializer=VoiteModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def voiteModelUpdate(request,pk):
    theObject=VoteModel.objects.get(pk=pk)
    serializer=VoiteModelSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})


@api_view(['GET'])
def voiteModelDetail(request,pk):
    theObject=VoteModel.objects.get(pk=pk)
    serializer=VoiteModelSerializer(theObject,many=False)
    return Response(serializer.data)





# qr eevnt
@api_view(['GET'])
def liveEventCommentList(request):
    objects=LiveEventComment.objects.all()
    serializer=LiveEventCommentSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def thisEventLiveEventCommentList(request,pk):
    objects=LiveEventComment.objects.filter(theEvent=EventView.objects.get(pk=pk))
    serializer=LiveEventCommentSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def liveEventCommentCreate(request):
    serializer=LiveEventCommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def liveEventCommentUpdate(request,pk):
    theObject=LiveEventComment.objects.get(pk=pk)
    serializer=LiveEventCommentSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def liveEventCommentDelete(request,pk):
    theObject=LiveEventComment.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def liveEventCommentDetail(request,pk):
    theObject=LiveEventComment.objects.get(pk=pk)
    serializer=LiveEventCommentSerializer(theObject,many=False)
    return Response(serializer.data)






# qr eevnt
@api_view(['GET'])
def lessonAnswersList(request):
    objects=LessonAnswers.objects.all()
    serializer=LessonAnswersSerializer(objects,many=True)
    return Response(serializer.data)


@api_view(['POST','GET'])
def lessonAnswersCreate(request):
    serializer=LessonAnswersCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def lessonAnswersUpdate(request,pk):
    theObject=LessonAnswers.objects.get(pk=pk)
    serializer=LessonAnswersSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})


@api_view(['DELETE'])
def lessonAnswersDelete(request,pk):
    theObject=LessonAnswers.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def lessonAnswersDetail(request,pk):
    theObject=LessonAnswers.objects.get(pk=pk)
    serializer=LessonAnswersSerializer(theObject,many=False)
    return Response(serializer.data)








@api_view(['GET'])
def qaPaidMoney(request,payType,usrNumber,amount,crsId,months,usrId):
    # direct payment
    if payType=='1':
        if InrolledCourse.objects.filter(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
            InrolledCourse.objects.create(
                theUser=UserProfile.objects.get(pk=usrId),
                theCourse=QaCourses.objects.get(pk=crsId),
                dateInrolled=datetime.now(),
                startDate=datetime.now(),
                endDate=datetime.now() + timedelta(days=30),
                courseProgress=0,
                stayedSeconds=0,
                itsLatestAccessedCourse=True
            )
            inrolledUserList= QaCourses.objects.get(pk=crsId)
            inrolledUserList.inrolledUsers.add(UserProfile.objects.get(pk=usrId))
            inrolledUserList.save()
            return Response({'status':True,'message':''})
        else:
            return Response({'status':True,'message':'This user is alerdy inrolled you can update it'})
    # waafi payment
    elif payType=='2':
        waafiUrl = 'https://api.waafipay.net/asm'
        jsonData = {
                "schemaVersion": "1.0",
                "requestId": "10111331033",
                "timestamp": "client_timestamp",
                "channelName": "WEB",
                "serviceName": "API_PURCHASE",
                "serviceParams": {
                    "merchantUid": "M0910291",
                    "apiUserId": "1000416",
                    "apiKey": "API-675418888AHX",
                    "paymentMethod": "mwallet_account",
                    "payerInfo": { "accountNo": '252'+usrNumber },
                    "transactionInfo": {
                        "referenceId": "12334",
                        "invoiceId": "7896504",
                        "amount": amount,
                        "currency": "USD",
                        "description": "Test USD"
                    }
                }
            }
        x = requests.post(waafiUrl, data = jsonData,headers= {"Content-Type":"application/json"})
        return Response({'status':x.status_code})
    # paybal and cr
    else:
        print('')
        return Response({'status':'papal'})
    

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def getThisCourseFirstLesson(courseId):
    thisCourseLessons=Lessons.objects.filter(theCourse=courseId)
    return thisCourseLessons[0]

@api_view(['POST'])
def inrollCourseToUser(request,paymentType):
    fullResp=''
    usrId=request.data['userId']
    usrNumber=request.data['number']
    usrMoney=request.data['money']
    crsId=request.data['courseId']
    months=request.data['months']
    referralCode=request.data['referralCode']
    cupponCode=request.data['cupponCode']
    # status=request.data['status']
    enrollingCourse=QaCourses.objects.get(pk=crsId)
    if enrollingCourse.itsFree or enrollingCourse.saledPrice == 0:
        try:
            if InrolledCourse.objects.filter(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
                print('cppp')
                theCourse= InrolledCourse.objects.create(
                    theUser=UserProfile.objects.get(pk=usrId),
                    theCourse=QaCourses.objects.get(pk=crsId),
                    dateInrolled=datetime.now(),
                    startDate=datetime.now(),
                    endDate=datetime.now() + timedelta(days=int(months)*30),
                    courseProgress=0,
                    currentLesson=getThisCourseFirstLesson(QaCourses.objects.get(pk=crsId)),
                    status=True,
                    stayedSeconds=0,
                    itsLatestAccessedCourse=True
                )
                inrolledUserList= QaCourses.objects.get(pk=crsId)
                inrolledUserList.inrolledUsers.add(UserProfile.objects.get(pk=usrId))
                inrolledUserList.save()
                fullResp={'paided':True,'status':'success','scopeId':theCourse.pk,'message':'Waad Ku Guuleesatay Iska Diiwaangalinta Courskan'}
            else:
                theCourse=InrolledCourse.objects.get(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId))
                theCourse.status=True
                theCourse.currentLesson=getThisCourseFirstLesson(theCourse.theCourse)
                theCourse.startDate=datetime.now()
                theCourse.endDate= (datetime.now() + timedelta(days=int(months)*30))
                print('inside')
                # theCourse.endDate=str(datetime.now() + timedelta(days=int(months)*30)).split(' ')[0]
                theCourse.save()
                fullResp={'paided':True,'courseInfo':{'courseTitle':theCourse.theCourse.title,'fromDate':theCourse.startDate,'toDate':theCourse.endDate},'status':'success','scopeId':theCourse.pk,'message':'Waad Ku Guuleesatay Iska Diiwaangalinta Courskan Markale'}
        except:
            fullResp={"status":False,"message":"course id or user id invalid"}

    else:
        paidResp=waafiPaidMoney(usrNumber,usrMoney)
        if paidResp['paided']:
            if InrolledCourse.objects.filter(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
                    theCourse= InrolledCourse.objects.create(
                        theUser=UserProfile.objects.get(pk=usrId),
                        theCourse=QaCourses.objects.get(pk=crsId),
                        dateInrolled=datetime.now(),
                        startDate=datetime.now(),
                        referralCode=referralCode,
                        cupponCode=cupponCode,
                        endDate=datetime.now() + timedelta(days=int(months)*30),
                        courseProgress=0,
                        currentLesson=getThisCourseFirstLesson(QaCourses.objects.get(pk=crsId)),
                        status=True,
                        stayedSeconds=0,
                        itsLatestAccessedCourse=True
                    )
                    inrolledUserList= QaCourses.objects.get(pk=crsId)
                    inrolledUserList.inrolledUsers.add(UserProfile.objects.get(pk=usrId))
                    inrolledUserList.save()
                    fullResp={'paided':True,'status':'success','scopeId':theCourse.pk,'message':'Waad Ku Guuleesatay Iska Diiwaangalinta Courskan'}
            else:
                theCourse=InrolledCourse.objects.get(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId))
                theCourse.status=True
                theCourse.currentLesson=getThisCourseFirstLesson(theCourse.theCourse)
                theCourse.startDate=datetime.now()
                theCourse.endDate= (datetime.now() + timedelta(days=int(months)*30))
                print('inside')
                # theCourse.endDate=str(datetime.now() + timedelta(days=int(months)*30)).split(' ')[0]
                theCourse.save()
                fullResp={'paided':True,'courseInfo':{'courseTitle':theCourse.theCourse.title,'fromDate':theCourse.startDate,'toDate':theCourse.endDate},'status':'success','scopeId':theCourse.pk,'message':'Waad Ku Guuleesatay Iska Diiwaangalinta Courskan Markale'}
        else:
            fullResp={'paided':False,'status':'failed','scopeId':'','message':'Processka lacag bixinta laguma guulaysan fadlan ku celi markale'}
    
    return Response(fullResp)


@api_view(['GET'])
def checkThisUserInrolledCourseSlug(request,usrId,slug):
    try:
        courseEnrolled = InrolledCourse.objects.filter(theCourse=QaCourses.objects.get(slug=slug)).filter(theUser=UserProfile.objects.get(pk=usrId))
        if courseEnrolled.exists():
            print('not exist')
            courseSerializer=QaCoursesSerializer(courseEnrolled[0].theCourse,many=False)
            return Response({'isEnrolled':True,'theCourse':courseSerializer.data})
        else:
            return Response({'isEnrolled':False,'theCourse':courseSerializer.data})
    except:
        try:
            courseSerializer=QaCoursesSerializer(QaCourses.objects.get(slug=slug),many=False)
            return Response({'isEnrolled':False,'theCourse':courseSerializer.data})
        except:
            return Response({'isEnrolled':False,'theCourse':'not exist'})




@api_view(['POST'])
def inrollEventToUser(request,paymentType):
    fullResp=''
    usrId=request.data['userId']
    usrNumber=request.data['number']
    usrMoney=request.data['money']
    evtId=request.data['evtId']
    enrollingEvent=EventView.objects.get(pk=evtId)
    if enrollingEvent.itsFree or enrollingEvent.price==0:
        try:
            if EventEnrolled.objects.filter(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
                theEvent= EventEnrolled.objects.create(
                    theUser=UserProfile.objects.get(pk=usrId),
                    theEvent=EventView.objects.get(pk=evtId),
                    paided=True,
                )
                # inrolledUserList= EventView.objects.get(pk=evtId)
                # inrolledUserList.enrolledStudents.add(UserProfile.objects.get(pk=usrId))
                # inrolledUserList.save()
                fullResp={'status':True,'alerdyInrolled':False,'scopeId':theEvent.pk,'message':'Waad ku guulaysatay iska diiwaangalinta eventigan'}
            else:
                print('arrrrr enrorr')
                theEvent=EventEnrolled.objects.get(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId))
                fullResp={'status':True,'alerdyInrolled':True,'scopeId':theEvent.pk,'message':'Waad ku guulaysatay iska diiwaangalinta eventigan'}
        except:
            fullResp={"status":False,"error":"user id not found"}
    else:
        paidResp=waafiPaidMoney(usrNumber,usrMoney)
        if paidResp['paided']:
            try:
                if EventEnrolled.objects.filter(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
                        theEvent= EventEnrolled.objects.create(
                            theUser=UserProfile.objects.get(pk=usrId),
                            theEvent=EventView.objects.get(pk=evtId),
                            paided=True,
                        )
                        inrolledUserList= EventView.objects.get(pk=evtId)
                        inrolledUserList.enrolledStudents.add(UserProfile.objects.get(pk=usrId))
                        inrolledUserList.save()
                        fullResp={'status':True,'alerdyInrolled':False,'scopeId':theEvent.pk,'message':'Waad ku guulaysatay iska diiwaangalinta eventigan'}
                else:
                    theEvent=EventEnrolled.objects.get(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId))
                    fullResp={'status':True,'alerdyInrolled':True,'scopeId':theEvent.pk,'message':'Waad ku guulaysatay iska diiwaangalinta eventigan'}
            except:
                fullResp = {"status":False,"error":"user id not found"}
        else:
            fullResp={'status':False,'alerdyInrolled':False,'scopeId':'','message':'Processka lacag bixinta laguma guulaysan fadlan ku celi markale'}

    return Response(fullResp)



@api_view(['GET'])
def checkThisUserInrolledEvent(request,usrId,evtId):
    eventEnrolled = EventEnrolled.objects.filter(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId))
    if eventEnrolled.exists():
        eventSerializer=EventViewSerializer((eventEnrolled.first()).theEvent,many=False)
        if (eventEnrolled.first()).paided==True:
            return Response({'paided':True,'exists':True,'theEvent':eventSerializer.data})
        else:
            return Response({'paided':False,'exists':True,'theEvent':eventSerializer.data})
    else:
        return Response({'paided':False,'exists':False})

@api_view(['GET'])
def checkThisUserInrolledEventSlug(request,usrId,slug):
    try:
        eventEnrolled = EventEnrolled.objects.filter(theEvent=(EventView.objects.filter(slug=slug).first()).pk,theUser=UserProfile.objects.get(pk=usrId))
        if eventEnrolled.exists():
            eventSerializer=EventViewSerializer((eventEnrolled.first()).theEvent,many=False)
            if (eventEnrolled.first()).paided==True:
                return Response({'paided':True,'isEnrolled':True,'exists':True,'theEvent':eventSerializer.data})
            else:
                return Response({'paided':False,'isEnrolled':True,'exists':True,'theEvent':eventSerializer.data})
        else:
            return Response({'paided':False,'isEnrolled':False,'exists':False,'theEvent':eventSerializer.data})
    except:
        try:
            eventSerializer=EventViewSerializer(EventView.objects.get(slug=slug),many=False)
            return Response({'paided':False,'isEnrolled':False,'exists':False,'theEvent':eventSerializer.data})
        except:
            return Response({'paided':False,'isEnrolled':False,'exists':False,'theEvent':'not exist'})





    
@api_view(['GET'])
def qSendMain(request,userProfilePK):
    # theUser = UserProfile.objects.get(pk=userProfilePK)
    # domain = get_current_site(request).domain
    # uidb64 = urlsafe_base64_encode(force_bytes(theUser.user.pk))
    # link =  reverse('usr-activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(theUser.user)})
    # activationLink='https://'+domain+link
    # if request.is_secure() == False:
    #     activationLink = 'http://'+domain+link
    # print(activationLink)
    # msg_html = render_to_string('invoice/email-activation.html', {'theUserName': theUser.fullName.split(' ')[0],'activationLink':activationLink})
    # emailStatus = send_mail(
    #     'Qaamuus Activation Code',
    #     msg_html,
    #     'Qaamuus Academy'+settings.EMAIL_HOST_USER,
    #     [theUser.email],
    # )
    return Response({'emailStatus':'emailStatus'}) 

@api_view(['GET'])
def getCurrentTime(request):
    return Response({'dateTimeNow':datetime.now()}) 

@api_view(['GET'])
def sendResetPasswordCode(request,username):
    sendedCode=random.randint(111111,999999)
    theUser=''
    status=400
    try:
        if username.find('@')!=-1:
            theUser=UserProfile.objects.get(email=username)
            msg_html = render_to_string('invoice/reset-password.html', {'theUserName': theUser.fullName.split(' ')[0],'sendedCode':(int(sendedCode)+int(theUser.pk))})
            text_content = strip_tags(msg_html)
            emailStatus = EmailMultiAlternatives(
                'Qaamuus Reset Password',
                text_content,
                'QAAMUUS ACADEMY '+settings.EMAIL_HOST_USER,
                [theUser.email],
            )
            emailStatus.attach_alternative(msg_html,"text/html")
            emailStatus.send()
            status=200
        else:
            theUser=UserProfile.objects.get(number=username)
            status='invalid email'
    except:
        status=100
        return Response({'sendedCode':sendedCode,'status':status,'theUserId':theUser.pk})
    
    return Response({'sendedCode':sendedCode,'status':status,'theUserId':theUser.pk})


    
@api_view(['GET'])
def sendActivationEmailCode(request,email):
    sendedCode=random.randint(111111,999999)
    msg_html = render_to_string('invoice/email-activation.html',{'theUserName':'Maxamed','activationLink':(int(sendedCode)+len(email))   })
    text_content = strip_tags(msg_html)
    emailStatus = EmailMultiAlternatives(
        'Qaamuus Activate Email',
        text_content,
        'QAAMUUS ACADEMY '+settings.EMAIL_HOST_USER,
        [email]
    )
    emailStatus.attach_alternative(msg_html,"text/html")
    emailStatus.send()
    status=200

    return Response({'sendedCode':sendedCode})




def waafiPaidMoney(usrNumber,usrMoney):
    theJsonData={
        "schemaVersion": "1.0",
        "requestId": "10111331033",
        "timestamp": "client_timestamp",
        "channelName": "WEB",
        "serviceName": "API_PURCHASE",
        "serviceParams": {
            "merchantUid": "M0910332",
            "apiUserId": "1000527",
            "apiKey": "API-1620730280AHX",
            "paymentMethod": "mwallet_account",
            "payerInfo": { "accountNo": '252'+usrNumber },
            "transactionInfo": {
                "referenceId": "12334",
                "invoiceId": "7896504",
                "amount": usrMoney,
                "currency": "USD",
                "description": "Test USD"
            }
        }
    }
    resp = requests.post('https://api.waafipay.net/asm',json=theJsonData,headers={ 'Content-type': 'application/json;charset=ISO-8859-1' })
    jsonPaidResp=json.loads(resp.text)
    if jsonPaidResp['responseCode']=='2001':
        return {'paided':True,'info':jsonPaidResp}
    else:
        return {'paided':False,'info':jsonPaidResp}

def eDahabPaidMoney(usrNumber,usrMoney):

    return Response({'paided':True})


