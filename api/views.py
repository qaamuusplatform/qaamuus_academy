from django.urls import reverse
from datetime import timedelta,datetime
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from itertools import chain
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse, response
from django.views import View
import requests
from django.contrib.auth.models import User
from a_webinar.models import EventView
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

@api_view(['POST'])
def jwtLogin(request):
    theUser=''
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username.find('@')!=-1:
        theUser=User.objects.filter(email=username).first()
    else:
        theUser=User.objects.filter(username=username).first()
    if theUser is None:
        raise AuthenticationFailed('User not found')

    if not theUser.check_password(password):
        raise AuthenticationFailed('Incorrect Password')


    payload={
        'id':theUser.id,
        'exp':datetime.utcnow()+timedelta(days=10),
        'iat':datetime.utcnow()
    }
    jwtToken=jwt.encode(payload,'secret',algorithm='HS256')
    
    jwtUserResponse=Response()
    jwtUserResponse.set_cookie(key='jwt',value=jwtToken,httponly=True)

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
def checkUserExistEmailAndUsername(request,username,email):
    isExist=True
    if User.objects.filter(username=username).exists()==False and User.objects.filter(email=email).exists()==False:
        isExist=False
    else:
        isExist=True
    
    # serializer=ClasseSerializer(classe,many=True)
    return Response({'isExist':isExist})





# userprofile
@api_view(['GET'])
def userProfileList(request):
    objects=UserProfile.objects.all()
    serializer=UserProfileSerializer(objects,many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def userProfileCreate(request):
    serializer=UserProfileCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['POST'])
def userProfileUpdate(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    serializer=UserProfileCreateSerializer(instance=theObject,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data})
    else:
        return Response({"status": "error", "data": serializer.errors})

@api_view(['DELETE'])
def userProfileDelete(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    
    theObject.delete()
    return Response()

@api_view(['GET'])
def userProfileDetail(request,pk):
    theObject=UserProfile.objects.get(pk=pk)
    serializer=UserProfileSerializer(theObject,many=False)
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
@api_view(['GET'])
def inrollCourseToUser(request,usrId,crsId,months,status):
    if InrolledCourse.objects.filter(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
            theCourse= InrolledCourse.objects.create(
                theUser=UserProfile.objects.get(pk=usrId),
                theCourse=QaCourses.objects.get(pk=crsId),
                dateInrolled=datetime.now(),
                startDate=datetime.now(),
                endDate=datetime.now() + timedelta(days=int(months)*30),
                courseProgress=0,
                currentLesson=getThisCourseFirstLesson(QaCourses.objects.get(pk=crsId)),
                status=str2bool(status),
                stayedSeconds=0,
                itsLatestAccessedCourse=True
            )
            inrolledUserList= QaCourses.objects.get(pk=crsId)
            inrolledUserList.inrolledUsers.add(UserProfile.objects.get(pk=usrId))
            inrolledUserList.save()
            return Response({'status':True,'scopeId':theCourse.pk,'message':'User Was Inrolled Registred Without Activation'})
    else:
        theCourse=InrolledCourse.objects.get(theCourse=crsId,theUser=UserProfile.objects.get(pk=usrId))
        theCourse.status=str2bool(status)
        theCourse.currentLesson=getThisCourseFirstLesson(theCourse.theCourse)
        theCourse.endDate=str(datetime.now() + timedelta(days=int(months)*30)).split(' ')[0]
        theCourse.save()
        return Response({'status':theCourse.status,'scopeId':theCourse.pk,'message':'This user is alerdy inrolled you can update it'})



    
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


    