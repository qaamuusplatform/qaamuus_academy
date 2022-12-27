from contextlib import nullcontext
from datetime import datetime, timedelta
from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# send email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
# from reportlab.lib.pagesizes import P
from django.core.paginator import Paginator
from django.db.models import Max
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from a_webinar.models import EventEnrolled, EventView
from api.models import *
from qaamuus_acd import settings

from .models import *


# Create your views here.
def indexWeb(request):
    qaCourses=QaCourses.objects.all()
    maxInrolled=QaCourses.objects.aggregate(Max('inrolledUsers'))
    maxInrolledCourse=''
    try:
        maxInrolledCourse=QaCourses.objects.filter(inrolledUsers=maxInrolled['inrolledUsers__max'])[0]
    except:
        maxInrolledCourse=''
    instructors=UserProfile.objects.filter(userType=2)
    # upComingEvents=EventView.objects.filter(dateTimeStarting____lte=datetime.now() + timedelta(days=1))
    upComingEvents=EventView.objects.filter(isPublic=True).filter(dateTimeStarting__gt =datetime.now())
    categorys=CourseCategory.objects.all()
    aboutQaamuusInfo = AboutQaamuusInfo.objects.all()[0]
    soonEvent=''
    try:
        soonEvent=upComingEvents[0]
    except:
        soonEvent=''
    activedFeedBacks=FeedBacks.objects.filter(isActive=True)
    ourInterFriends=OurInterFriends.objects.all()
    if request.user.is_authenticated:
        return render(request,'normal_pages/authHome.html',{'maxInrolledCourse':maxInrolledCourse,'aboutQaamuusInfo':aboutQaamuusInfo,'soonEvent':soonEvent,'upComingEvents':upComingEvents,'ourInterFriends':ourInterFriends,'qaCourses':qaCourses,'instructors':instructors,'categorys':categorys,'activedFeedBacks':activedFeedBacks})
    else:
        return render(request,'normal_pages/unAuthHome.html',{'maxInrolledCourse':maxInrolledCourse,'aboutQaamuusInfo':aboutQaamuusInfo,'soonEvent':soonEvent,'upComingEvents':upComingEvents,'ourInterFriends':ourInterFriends,'qaCourses':qaCourses,'instructors':instructors,'categorys':categorys,'activedFeedBacks':activedFeedBacks})



def qaCourses(request):
    allQaCourses=QaCourses.objects.all()
    courseCategory=CourseCategory.objects.all()
    activedFeedBacks=FeedBacks.objects.filter(isActive=True)
    return render(request,'manage/qa-courses.html',{'qaCourses':allQaCourses,'activedFeedBacks':activedFeedBacks,'courseCategory':courseCategory})

def qaCoursesCategory(request,categoryPk):
    allQaCourses=QaCourses.objects.filter(category=categoryPk)
    courseCategory=CourseCategory.objects.all()
    activedFeedBacks=FeedBacks.objects.filter(isActive=True)
    return render(request,'manage/qa-courses.html',{'qaCourses':allQaCourses,'activedFeedBacks':activedFeedBacks,'courseCategory':courseCategory})


@login_required(login_url='/sing-in/')
def crsDtlWth(request,pk,encTitle):
    courseDetail=QaCourses.objects.get(pk=pk)
    isInrolledBefore=False
    inrolledBefore=''
    try:
        inrolledBefore=InrolledCourse.objects.get(theCourse=pk,theUser=UserProfile.objects.get(user=request.user.pk))
        isInrolledBefore=InrolledCourse.objects.filter(theCourse=pk,theUser=UserProfile.objects.get(user=request.user.pk)).exists()
    except:
        isInrolledBefore=False
    compos=lessonCompo.objects.filter(theCourse=courseDetail).order_by('compoName')
    courseLessons=Lessons.objects.filter(theCourse=courseDetail).order_by('lessonNum')
    activedFeedBacks=FeedBacks.objects.filter(isActive=True)
    courseReview=CourseReview.objects.filter(theCourse=courseDetail)
    return render(request,'detail/course-detail.html',{'courseReview':courseReview,'compos':compos,'inrolledBefore':inrolledBefore,'isInrolledBefore':isInrolledBefore,'courseDetail':courseDetail,'courseLessons':courseLessons,'activedFeedBacks':activedFeedBacks})


@login_required(login_url='/sing-in/')
def myCourses(request,pk,encTitle):
    # inrolledEvents=EventEnrolled.objects.filter(theUser=UserProfile.objects.get(pk=usrId))
    
    inrollmentCourses=InrolledCourse.objects.filter(theUser=UserProfile.objects.get(pk=pk))
    return render(request,'detail/my-courses.html',{'inrollmentCourses':inrollmentCourses,'exists':True,'latestAccessedCourse':inrollmentCourses.get(itsLatestAccessedCourse=True)})

@login_required(login_url='/sing-in/')
def paymentPage(request,searchKey,pk,encTitle):
    isInrolledBefore=InrolledCourse.objects.filter(theCourse=pk,theUser=UserProfile.objects.get(user=request.user.pk))
    courseDetail=QaCourses.objects.get(pk=pk)
    return render(request,'detail/payment-page.html',{'courseDetail':courseDetail,'isInrolledBefore':isInrolledBefore})


def getThisCourseLessons(courseLessons):
    lessonsTopics=''
    allTopics=Topic.objects.all()
    for lsn in courseLessons:
        theLessonTopcs=Topic.objects.filter(theLesson=Lessons.objects.get(pk=lsn.pk))
        lessonsTopics=list(chain(lessonsTopics, theLessonTopcs))
    return lessonsTopics


@login_required(login_url='/sing-in/')
def courseTakeInrolledLesson(request,crsPk,encTitle,lessonId):
    courseDetail=QaCourses.objects.get(pk=crsPk)
    inrollmentCourses=InrolledCourse.objects.filter(theUser=UserProfile.objects.get(user=User.objects.get(pk=request.user.pk)))
    for inrCrs in inrollmentCourses:
        if inrCrs.theCourse==courseDetail:
            inrCrs.itsLatestAccessedCourse=True
        else:
            inrCrs.itsLatestAccessedCourse=False
        inrCrs.save()
    if inrollmentCourses.get(theCourse=QaCourses.objects.get(pk=crsPk)).status:
        inrollmentCourses.get(theCourse=QaCourses.objects.get(pk=crsPk)).currentLesson=Lessons.objects.get(pk=lessonId)
        inrollmentCourses.get(theCourse=QaCourses.objects.get(pk=crsPk)).save()
        currentLesson=Lessons.objects.get(pk=lessonId)
        courseLessons=Lessons.objects.filter(theCourse=courseDetail)
        lessonsTopics=Topic.objects.filter(theLesson=currentLesson)
        lessonDiscussion=LessonDiscussion.objects.filter(theLesson=currentLesson)
        return render(request,'inrollment/lessons-inroll copy.html',{'courseDetail':courseDetail,'courseLessons':courseLessons,'lessonDiscussions':lessonDiscussion,'currentLesson':currentLesson,'lessonsTopics':lessonsTopics})
    else:
        return render(request,'detail/payment-page.html',{'courseDetail':courseDetail})
    

@login_required(login_url='/sing-in/')
def discussionDetail(request,discId):
    theDiscussion=LessonDiscussion.objects.get(pk=discId)
    lessonAnswers = LessonAnswers.objects.filter(theDiscussion=theDiscussion)
    return render(request,'detail/discussion_detail.html',{'theDiscussion':theDiscussion,'lessonAnswers':lessonAnswers})

def liveTheAnswer(request,answId,userId,discId):
    theAnswer=LessonAnswers.objects.get(pk=answId)
    if UserProfile.objects.get(pk=userId) in theAnswer.likedTheAnswer.all():
        theAnswer.likedTheAnswer.remove(UserProfile.objects.get(pk=userId))
        print('yesss')
    else:
        theAnswer.likedTheAnswer.add(UserProfile.objects.get(pk=userId))
        print('nooo ')
    return HttpResponseRedirect('/discussion-detail/'+discId+'/')
# @login_required(login_url='/sing-in/')
# def postAnswer(request,userId,discId):
#     LessonAnswers.objects.create(
#        theUser= userId,
#        theDiscussion=discId,

#     )
#     return render(request,'detail/discussion_detail.html',{'theDiscussion':theDiscussion,'lessonAnswers':lessonAnswers})





def events(request):
    events=EventView.objects.filter(isPublic=True).all()
    upComingEvents=EventView.objects.filter(isPublic=True).filter(dateTimeStarting__gt = datetime.now())
    print('upComingEvents')
    print(upComingEvents)
    return render(request,'manage/events.html',{'events':events,'upComingEvents':upComingEvents})

def eventDetail(request,pk,enc1):
    review=CourseReview.objects.filter(theCourse=pk)
    theEvent=EventView.objects.get(pk=pk)
    isInrolledBefore=True
    try:
        isInrolledBefore=EventEnrolled.objects.filter(theEvent=pk,theUser=UserProfile.objects.get(user=request.user.pk)).exists()
    except:
        isInrolledBefore=False
    dateTimeStarting=str(theEvent.dateTimeStarting)
    modDateTimeStream=dateTimeStarting.split(' ')[0].replace('-','/') +' '+ dateTimeStarting.split(' ')[1].split('+')[0]
    # print(theEvent.dateTimeStarting)
    # print('time zone',datetime.utcnow())
    # print(datetime.now())
    # print(timezone.now())
    # print(theEvent.dateTimeStarting-timezone.now())
    return render(request,'detail/event-detail.html',{'review':review,'isInrolledBefore':isInrolledBefore,'theEvent':theEvent,'modDateTimeStream':modDateTimeStream})

@login_required(login_url='/sing-in/')
def eventComminTimer(request,enc1,evtId,enc2):
    theEvent=EventView.objects.get(pk=evtId)
    dateTimeStarting=str(theEvent.dateTimeStarting)
    userEventInrolment=False
    try:
        if EventEnrolled.objects.filter(theEvent=theEvent).filter(paided=True).filter(theUser=UserProfile.objects.get(user=request.user.pk)).exists():
            userEventInrolment=True
        else:
            userEventInrolment=False
    except:
        userEventInrolment=False
    modDateTimeStream=dateTimeStarting.split(' ')[0].replace('-','/') +' '+ dateTimeStarting.split(' ')[1].split('+')[0]
    return render(request,'detail/event-commin-soon.html',{'theEvent':theEvent,'modDateTimeStream':modDateTimeStream,'userEventInrolment':userEventInrolment})

@login_required(login_url='/sing-in/')
def webinarLive(request,evtId,evtTitle):
    theEvent=EventView.objects.get(pk=evtId)
    # print(str(theEvent.dateTimeStarting).split(':')[0]+str(theEvent.dateTimeStarting).split(':')[1])
    if EventEnrolled.objects.filter(theUser=UserProfile.objects.get(user=request.user),theEvent=theEvent).exists():
        if EventEnrolled.objects.get(theUser=UserProfile.objects.get(user=request.user),theEvent=theEvent).paided==True:
            return render(request,'inrollment/event-inrolled copy.html',{'theEvent':theEvent})
        else:
            return redirect('/event-detail/'+evtId+'/'+theEvent.title+'/')
    else:
        return redirect('/event-detail/'+evtId+'/'+theEvent.title+'/')
    # if theEvent.dateTimeStarting > datetime.now():
    #     # eventLiveComment=liveEventComment.objects.filter(theEvent=theEvent)
    #     return render(request,'inrollment/event-inrolled.html',{'theEvent':theEvent})
    # else:
    #     return HttpResponseRedirect('/event-commin-timer/'+str(theEvent.title)+'/'+str(theEvent.pk)+'/'+str(theEvent.eventType)+'/')

@login_required(login_url='/sing-in/')
def webinarLiveMeeting(request,evtId):
    theEvent=EventView.objects.get(pk=evtId)
    if EventEnrolled.objects.filter(theUser=UserProfile.objects.get(user=request.user),theEvent=theEvent).exists():
        if EventEnrolled.objects.get(theUser=UserProfile.objects.get(user=request.user),theEvent=theEvent).paided==True:
           return render(request,'webinar/meeting.html',{'theEvent':theEvent})
        else:
            return redirect('/event-detail/'+evtId+'/'+theEvent.title+'/')
    else:
        return redirect('/event-detail/'+evtId+'/'+theEvent.title+'/')
    


def getLatestAccessedCourse(usrId):
    latestCourseExist=False
    inrollmentCourses=InrolledCourse.objects.filter(theUser=UserProfile.objects.get(pk=usrId))
    
    try:
        inrollmentCourses.get(itsLatestAccessedCourse=True)
        latestCourseExist=True
    except:
        latestCourseExist=False
        
    return latestCourseExist

@login_required(login_url='/sing-in/')
def usrDashboard(request,enc1,usrId,enc2):
    inrollmentCourses=InrolledCourse.objects.filter(theUser=UserProfile.objects.get(pk=usrId))
    relatedCourses=QaCourses.objects.filter().all()
    recentCourses=QaCourses.objects.filter().all()
    inrolledEvents=EventEnrolled.objects.filter(theUser=UserProfile.objects.get(pk=usrId))
    userDiscussion=LessonDiscussion.objects.filter(theUser=UserProfile.objects.get(pk=usrId))
    # set up paginator
    discPagin=Paginator(userDiscussion,5)
    discPage=request.GET.get('discPage')
    pagingDescs=discPagin.get_page(discPage)
    if getLatestAccessedCourse(usrId):
        return render(request,'detail/user-detail-dash.html',{'inrolledEvents':inrolledEvents,'recentCourses':recentCourses,'relatedCourses':relatedCourses,'events':'','userDiscussion':pagingDescs,'inrollmentCourses':inrollmentCourses,'exists':True,'latestAccessedCourse':inrollmentCourses.get(itsLatestAccessedCourse=True)})
    else: 
        return render(request,'detail/user-detail-dash.html',{'inrolledEvents':inrolledEvents,'recentCourses':recentCourses,'relatedCourses':relatedCourses,'events':'','userDiscussion':pagingDescs,'inrollmentCourses':inrollmentCourses,'exists':False})

def singIn(request):
    status = ''
    userIsActive=0
    theUser=''
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username.find('@')!=-1:
            userIsActive=userIsActiveFun(True,username)
            theUser=getThisUserId(True,username)
            username=getUserByEmail(username)
        else:
            userIsActive=userIsActiveFun(False,username)
        user = authenticate(request,username=username,password=password)
        print(userIsActive)
        print('uuu')
        theUser=getThisUserId(False,username)
        if user is not None:
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('/')
        else:
            status='The Username or Password is Incorrect'            

    return render(request,'normal_pages/sing-in.html',{'status':status,'userIsActive':userIsActive,'theUser':theUser})

def userIsActiveFun(isEmail,username):
    userIsActive=0
    try:
        if isEmail:
            if UserProfile.objects.get(email=username).user_activated:
                userIsActive=1
            else:
                userIsActive=0
        else:
            if UserProfile.objects.get(number=username).user_activated:
                userIsActive=1
            else:
                userIsActive=0
    except:
        print('not exist')
        userIsActive=3

    return userIsActive

def getThisUserId(isEmail,username):
    theUser=0
    try:
        if isEmail:
            theUser=UserProfile.objects.get(email=username)
        else:
            theUser=UserProfile.objects.get(number=username)
    except:
        print('not exist')
        theUser

    return theUser

def getUserByEmail(email):
    username=''
    if UserProfile.objects.filter(email=email).exists():
        username=UserProfile.objects.get(email=email).user.username
        
    return username
def registerNu(request):
    return render(request,'normal_pages/register-nu.html')

def instructorInfo(request,usrId,enc1):
    instructorInfo=UserProfile.objects.get(pk=usrId)
    if instructorInfo.userType == UserTypes.objects.get(pk=2):
        instructorCertification=InstructorCertification.objects.filter(theUser=instructorInfo)
        instructorCourses=QaCourses.objects.filter(instructor=instructorInfo)
        
        return render(request,'detail/instructor-detail.html',{'instructorCertification':instructorCertification,'instructorInfo':instructorInfo,'instructorCourses':instructorCourses})
    else:
        return redirect('/instructors/')
@login_required(login_url='/sing-in/')
def usrEdit(request,enc1,usrId,enc2):
    userProfileInfo=UserProfile.objects.get(pk=usrId)
    return render(request,'detail/user-profile-edit.html',{'userProfileInfo':userProfileInfo})

def logouThisUser(request):
    logout(request)
    return HttpResponseRedirect('/')




def sendActivationEmail(request,usrId):
    theUser = UserProfile.objects.get(user=User.objects.get(pk=usrId))
    domain = get_current_site(request).domain
    time_now = datetime.now()
    expiration_time = time_now+timedelta(minutes=5)
    round_of_exp_time = round(expiration_time.timestamp())
    link='/email/activation/{}/{}/'.format(theUser.pk,round_of_exp_time)
    activationLink='https://'+domain+link
    if request.is_secure() == False:
        activationLink = 'http://'+domain+link
    msg_html = render_to_string('invoice/email-activation.html', {'theUserName': theUser.fullName.split(' ')[0],'activationLink':activationLink})
    text_content = strip_tags(msg_html)

    emailStatus = EmailMultiAlternatives(
        'Qaamuus Activation Code',
        text_content,
        'QAAMUUS ACADEMY '+settings.EMAIL_HOST_USER,
        [theUser.email],
    )
    emailStatus.attach_alternative(msg_html,"text/html")
    emailStatus.send()
    return render(request,'normal_pages/sing-in.html',{'activeLinkSended':True,'theUser':theUser})





def activateEmail(request,usrId,timeAsMap):
    theUser=UserProfile.objects.get(pk=usrId)
    usr=User.objects.get(pk=theUser.user.pk)
    if theUser.user_activated and usr.is_active:
        return redirect('/sing-in/')
    else:
        time_now = datetime.now()
        expiration_time = time_now+timedelta()
        round_of_exp_time = round(expiration_time.timestamp())
        if round_of_exp_time>timeAsMap:
            print('time now bigger is exipred')
        else:
            theUser.user_activated=True
            theUser.save()
            usr.is_active=True
            usr.save()
            print(usr.is_active)
        return render(request,'normal_pages/sing-in.html',{'userIsActive':True})

def passwordReset(request):
    return render(request,'normal_pages/password_reset.html')



def createNewPassword(request,usrId):
    theUser=UserProfile.objects.get(pk=usrId)
    usr=User.objects.get(pk=theUser.user.pk)
    if request.POST:
        password=request.POST.get('password')
        passwordComfirm=request.POST.get('passwordComfirm')
        if password==passwordComfirm:
            theUser.password=password
            theUser.save()
            usr.password=password
            usr.set_password(usr.password)
            usr.save()
            return redirect('/sing-in/')
        else:
            return render(request,'normal_pages/create-password.html',{'status':'password and comfirm password not match','usrId':usrId})
    else:
        return render(request,'normal_pages/create-password.html',{'usrId':usrId})

def instructor(request):
    instructors=UserProfile.objects.filter(userType=2)
    return render(request,'manage/instructor.html',{'instructors':instructors})





def livePreparing(request,theEventPk):
    theEvent=EventView.objects.get(pk=theEventPk)
    return render(request,'webinar/sdk-signature.html',{'theEvent':theEvent})








def voteScreen(request):
    return render(request,'normal_pages/voit-page.html',{'registred':True})
    

def handled_not_found(request,exception):
    return render(request,'not-found.html')

def userProfileInfo(request):
    if(request.user.pk==None):
        return {
            'userInfo':{}
        }
    elif(request.user.pk==nullcontext):
        return {
                'userInfo':{}
            }
    else:
        try:
            if(UserProfile.objects.filter(user=User.objects.get(pk=request.user.id)).exists()==True):
                return {
                    'userInfo': UserProfile.objects.get(user=User.objects.get(pk=request.user.id))
                }
            else:
                return {
                    'userInfo': ''
                }
        except:
            return {
                    'userInfo': ''
                }
        