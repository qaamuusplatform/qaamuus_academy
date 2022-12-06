from django.db import models
from ckeditor.fields import RichTextField
from api.models import *

import jwt
import datetime
import requests
import json

# Create your models here.



def createMeeting(theMeetingDetail):
    time_now = datetime.datetime.now()
    expiration_time = time_now+datetime.timedelta(seconds=50)
    round_of_exp_time = round(expiration_time.timestamp())

    headers = {"alg":"H5256","type":"JWT"}
    payload = {"iss": "Qq1J6N5yRZCU9KAQ9_696Q","exp": round_of_exp_time}

    encoded_jwt = jwt.encode(payload,"JHDx2uOli3phxSlO72SbT4ZZMX282YZEEFi8", algorithm="HS256")
    email = 'maxamedltc@gmail.com'

    url = 'https://api.zoom.us/v2/users/{}/meetings'.format(email)
    headerD = {"authorization":"Bearer {}".format(encoded_jwt)}
    created_meeting = requests.post(url,json=theMeetingDetail,headers=headerD)
    return json.loads(created_meeting.text)

def updateMeeting(meetingId,theMeetingDetail):
    time_now = datetime.datetime.now()
    expiration_time = time_now+datetime.timedelta(seconds=50)
    round_of_exp_time = round(expiration_time.timestamp())

    headers = {"alg":"H5256","type":"JWT"}
    payload = {"iss": "Qq1J6N5yRZCU9KAQ9_696Q","exp": round_of_exp_time}

    encoded_jwt = jwt.encode(payload,"JHDx2uOli3phxSlO72SbT4ZZMX282YZEEFi8", algorithm="HS256")
    email = 'maxamedltc@gmail.com'

    url = 'https://api.zoom.us/v2/users/{}/meetings/'.format(email,meetingId)
    headerD = {"authorization":"Bearer {}".format(encoded_jwt),'occurrence_id':'JVJasiOkSi2JtDVUMv+cyQ=='}
    updated_meeting = requests.patch(url,json=theMeetingDetail,headers=headerD)
    # print(updated_meeting.headers)
    # print(updated_meeting._content)
    # print(updated_meeting.history)
    # print(updated_meeting)
    return updated_meeting

def getMeetingDetail(meetingId):
    print('meetingi',meetingId)
    time_now = datetime.datetime.now()
    expiration_time = time_now+datetime.timedelta(seconds=50)
    round_of_exp_time = round(expiration_time.timestamp())

    headers = {"alg":"H5256","type":"JWT"}
    payload = {"iss": "Qq1J6N5yRZCU9KAQ9_696Q","exp": round_of_exp_time}

    encoded_jwt = jwt.encode(payload,"JHDx2uOli3phxSlO72SbT4ZZMX282YZEEFi8", algorithm="HS256")
    email = 'maxamedltc@gmail.com'

    url = 'https://api.zoom.us/v2/users/{}/meetings/81898979846'.format(email)
    headerD = {"authorization":"Bearer {}".format(encoded_jwt)}
    updated_meeting = requests.get(url,headers=headerD)
    print(updated_meeting)
    return updated_meeting


class EventView(models.Model):
    title=models.CharField(max_length=255)
    slag=models.CharField(max_length=2555,default='')
    simDesc=models.CharField(max_length=255,null=True,blank=True)
    desc=RichTextField(blank=True,null=True)
    dataRegistred=models.DateTimeField(auto_now=True)
    prevVideo=models.CharField(max_length=2000)
    coverImage=models.ImageField(upload_to='images/events',null=True,blank=True)
    image=models.ImageField(upload_to='images/events',null=True,blank=True)
    videoUrl=models.CharField(max_length=50000,default='https://qcdn.qaamuus.academy/media/video/videoUploaded/Akaadeemiyadda_Qaamuus.mp4')
    isRealLiveSdk=models.BooleanField(default=False)
    isLiveIcon=models.BooleanField(default=False)
    isEnded=models.BooleanField(default=False)
    eventType=models.CharField(max_length=255)
    persenter=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    dateTimeStarting=models.DateTimeField()
    language=models.CharField(max_length=255)
    level=models.CharField(max_length=255)
    meetingNumber=models.CharField(max_length=255,blank=True)
    meetingPassword=models.CharField(max_length=255,blank=True)
    join_URL=models.CharField(max_length=555,blank=True)
    duration=models.CharField(max_length=255)
    itsFree=models.BooleanField(default=False)
    price=models.FloatField(default=0)
    isPublic=models.BooleanField(default=True)
    heroEvent=models.BooleanField(default=False)
    enrolledStudents=models.ManyToManyField(UserProfile,related_name='members')

    def __str__(self) -> str:
        return str(self.pk)+ str(self.title)+' -- '+str(self.simDesc)

class EventEnrolled(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theEvent=models.ForeignKey(EventView,on_delete=models.CASCADE)
    paided=models.BooleanField(default=True)
    paymentMethod=models.CharField(max_length=25,null=True,blank=True)
    dateTr=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.theUser.fullName)+' -- '+str(self.theEvent.title)

    
class LiveEventComment(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theEvent=models.ForeignKey(EventView,on_delete=models.CASCADE)
    commentText=models.TextField(null=True,blank=True)
    dateTr=models.DateTimeField(auto_now=True)
    




# a token and meeting details


# def createMeeting(meetingdetails):
# 	headers = {'authorization': 'Bearer ' + generateToken(),
# 			'content-type': 'application/json'}
# 	r = requests.post(
# 		f'https://api.zoom.us/v2/users/me/meetings',
# 		headers=headers, data=json.dumps(meetingdetails))

# 	y = json.loads(r.text)
# 	join_URL = y["join_url"]
# 	meetingPassword = y["password"]

# 	print(
# 		f'\n here is your zoom meeting link {join_URL} and your \
# 		password: "{meetingPassword}"\n')

# def updateMeeting(meetingdetails):
# 	headers = {'authorization': 'Bearer ' + generateToken(),
# 			'content-type': 'application/json'}
# 	r = requests.post(
# 		f'https://api.zoom.us/v2/users/me/meetings',
# 		headers=headers, data=json.dumps(meetingdetails))

# 	y = json.loads(r.text)
# 	join_URL = y["join_url"]
# 	meetingPassword = y["password"]
# 	print(
# 		f'\n here is your zoom meeting link {join_URL} and your \
# 		password: "{y}"\n')

