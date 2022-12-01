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

    def save(self,*args,**kwargs):
        if self._state.adding:
            if self.isRealLiveSdk:
                theMeetingDetail={"topic":self.title,
                        "start_time":self.dateTimeStarting.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "agenda": self.eventType,
                        "duration":40,
                        "timezone": "Africa/Mogadishu",
                        "settings":{
                            "host_video":"false",
                            "participant_video":"false",
                            "cn_meeting":"false",
                            "in_meeting":"false",
                            "join_before_host":"false",
                            "jbh_time":0,
                            "mute_upon_entry":"false",
                            "watermark":"false",
                            "use_pmi":"false",
                            "approval_type":2,
                            "audio":"voip",
                            "auto_recording":"none",
                            "enforce_login":"false",
                            "enforce_login_domains":"",
                            "alternative_hosts":"",
                            "alternative_host_update_polls":"false",
                            "close_registration":"false",
                            "show_share_button":"false",
                            "allow_multiple_devices":"false",
                            "registrants_confirmation_email":"true",
                            "waiting_room":"false",
                            "request_permission_to_unmute_participants":"false",
                            "registrants_email_notification":"true",
                            "meeting_authentication":"false",
                            "encryption_type":"enhanced_encryption",
                            "approved_or_denied_countries_or_regions":{
                                "enable":"false"
                            },
                            "breakout_room":{
                                "enable":"false"
                            },
                            "alternative_hosts_email_notification":"true",
                            "device_testing":"false",
                            "focus_mode":"false",
                            "private_meeting":"false",
                            "email_notification":"true",
                            "host_save_video_order":"false"
                        },
                }
                createdMeeting=createMeeting(theMeetingDetail)
                print('is created',createdMeeting)
                self.meetingNumber=createdMeeting["id"]
                self.meetingPassword=createdMeeting["password"]
                self.join_URL=createdMeeting["join_url"]
            # self.save()
        else:
            datetime.datetime.now().strftime
            # theMeetingDetail={"topic":self.title,
            #         "start_time":self.dateTimeStarting.strftime("%Y-%m-%dT%H:%M:%SZ"),
            #         "agenda": self.eventType,
            #         "duration":40,
            #         "timezone": "Africa/Mogadishu",
            #         "settings":{
            #             "host_video":"false",
            #             "participant_video":"false",
            #             "cn_meeting":"false",
            #             "in_meeting":"false",
            #             "join_before_host":"false",
            #             "jbh_time":0,
            #             "mute_upon_entry":"false",
            #             "watermark":"false",
            #             "use_pmi":"false",
            #             "approval_type":2,
            #             "audio":"voip",
            #             "auto_recording":"none",
            #             "enforce_login":"false",
            #             "enforce_login_domains":"",
            #             "alternative_hosts":"",
            #             "alternative_host_update_polls":"false",
            #             "close_registration":"false",
            #             "show_share_button":"false",
            #             "allow_multiple_devices":"false",
            #             "registrants_confirmation_email":"true",
            #             "waiting_room":"false",
            #             "request_permission_to_unmute_participants":"false",
            #             "registrants_email_notification":"true",
            #             "meeting_authentication":"false",
            #             "encryption_type":"enhanced_encryption",
            #             "approved_or_denied_countries_or_regions":{
            #                 "enable":"false"
            #             },
            #             "breakout_room":{
            #                 "enable":"false"
            #             },
            #             "alternative_hosts_email_notification":"true",
            #             "device_testing":"false",
            #             "focus_mode":"false",
            #             "private_meeting":"false",
            #             "email_notification":"true",
            #             "host_save_video_order":"false"
            #         },
                    
            # }
            # updatedMeeting=updateMeeting(self.meetingNumber,theMeetingDetail)
            print('updated')
            # updatedMeeting=getMeetingDetail(self.meetingNumber)
            # self.meetingNumber=createdMeeting["id"]
            # print(updatedMeeting)
            # self.meetingPassword=createdMeeting["password"]
            # self.join_URL=createdMeeting["join_url"]
        return super().save()
    
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

