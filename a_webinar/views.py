from django.shortcuts import render

from rest_framework.decorators import api_view
from a_system.models import OurInterFriends
from rest_framework.response import Response
from a_webinar.models import *
from api.models import *

# Create your views here.
def qaEvents(request):
    ourInterFriends= OurInterFriends.objects.all()
    studentsFeedbacks=FeedBacks.objects.filter(isActive=True)
    instroctors=UserProfile.objects.filter(userType=1)
    events=EventView.objects.filter(isPublic=True).all()
    return render(request,'webinar/qa-events.html',{'events':events,'instroctors':instroctors,'studentsFeedbacks':studentsFeedbacks,'ourInterFriends':ourInterFriends})

# def qaEvents(request):
#     return render(request,'webinar/qa-events.html')

def eventDetail(request,pk):
    theEventDetail=EventView.objects.get(pk=pk)
    return render(request,'webinar/event-detail.html',{'theEventDetail':theEventDetail})
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@api_view(['GET'])
def inrollEventToUser(request,usrId,evtId,status):
    if EventEnrolled.objects.filter(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId)).exists()==False:
            theEvent= EventEnrolled.objects.create(
                theUser=UserProfile.objects.get(pk=usrId),
                theEvent=EventView.objects.get(pk=evtId),
                paided=str2bool(status),
            )
            inrolledUserList= EventView.objects.get(pk=evtId)
            inrolledUserList.enrolledStudents.add(UserProfile.objects.get(pk=usrId))
            inrolledUserList.save()
            return Response({'status':True,'alerdyInrolled':False,'scopeId':theEvent.pk,'message':'User Was Inrolled Registred Without Activation'})
    else:
        theEvent=EventEnrolled.objects.get(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId))
        return Response({'status':True,'alerdyInrolled':True,'scopeId':theEvent.pk,'message':'This user is alerdy inrolled you can update it'})

    
@api_view(['GET'])
def checkThisUserInrolledEvent(request,usrId,evtId):
    if EventEnrolled.objects.filter(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId)).exists():
        if EventEnrolled.objects.get(theEvent=evtId,theUser=UserProfile.objects.get(pk=usrId)).paided==True:
            return Response({'paided':True,'exists':True})
        else:
            return Response({'paided':False,'exists':True})
    else:
        return Response({'paided':False,'exists':False})

