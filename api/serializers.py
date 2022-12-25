from django.contrib.auth.models import User
from rest_framework import serializers
from a_system.models import OurInterFriends

from a_webinar.models import *

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
class InstructorCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=InstructorCertification
        fields='__all__'


class UserProfileCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=UserProfile
        fields='__all__'

class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserNotifications
        fields='__all__'
        depth=2

class UserProfileSerializer(serializers.ModelSerializer):
    theCertifications=InstructorCertificationSerializer(read_only=True,many=True)
    theNotifications=UserNotificationsSerializer(read_only=True,many=True)
    class Meta:
        model=UserProfile
        fields='__all__'
        depth=2

class UnAuthUserProfileSerializer(serializers.ModelSerializer):
    
    theCertifications=InstructorCertificationSerializer(read_only=True,many=True)
    class Meta:
        model=UserProfile
        fields=['pk','fullName','profileImage','userTitle','userType','theCertifications']
        depth=2
class OurInterFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OurInterFriends
        fields='__all__'
        depth=1

class EventReviewSerializer(serializers.ModelSerializer):
    theUser=UnAuthUserProfileSerializer()
    class Meta:
        model=EventReview
        fields=['theEvent','theUser','theText','theRate','dateTime']
        depth=1

class EventViewSerializer(serializers.ModelSerializer):
    theReviews=EventReviewSerializer(read_only=True,many=True)
    persenter=UnAuthUserProfileSerializer()
    class Meta:
        model=EventView
        fields=['pk','title','slug','persenter','coHosts','theReviews','simDesc','desc','prevVideo','image','language','level','duration','heroEvent','isPublic','price','itsFree','discountPrice','discountPrice','isLiveIcon','isEnded','eventType','videoUrl','coverImage','dateTimeStarting']
        depth=2

class FeedBacksSerializer(serializers.ModelSerializer):
    class Meta:
        model=FeedBacks
        fields='__all__'
        depth=1



class AnswerDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'
        depth=1

class LessonDiscussionSerializer(serializers.ModelSerializer):
    dateSince=serializers.ReadOnlyField(source='date|timesince')
    theDiscussionAnswers=AnswerDiscussionSerializer(read_only=True,many=True)
    class Meta:
        model=LessonDiscussion
        fields='__all__'
        depth=1

class LessonsSerializer(serializers.ModelSerializer):
    theDiscussions=LessonDiscussionSerializer(read_only=True,many=True)
    class Meta:
        model=Lessons
        fields='__all__'
        depth=1



class LessonsUnAuthSerializer(serializers.ModelSerializer):
    theDiscussions=LessonDiscussionSerializer(read_only=True,many=True)
    class Meta:
        model=Lessons
        fields=['title','lessonNum','simDesc','fullDesc','duration','fullDesc','lessonVideo','lessonLink','dateRegistred','theDiscussions']
        depth=1


class lessonCompoSerializer(serializers.ModelSerializer):
    theCompoLessons=LessonsUnAuthSerializer(read_only=True,many=True)
    class Meta:
        model=lessonCompo
        fields=['id','compoName','lessonsCount','totalHours','theCompoLessons','simDesc']
        depth=1






class CourseReviewSerializer(serializers.ModelSerializer):
    
    theUser=UnAuthUserProfileSerializer()
    class Meta:
        model=CourseReview
        fields=['theCourse','theUser','theText','theRate','dateTime']
        depth=1



class QaCoursesSerializer(serializers.ModelSerializer):
    theComponents=lessonCompoSerializer(read_only=True,many=True)
    theReviews=CourseReviewSerializer(read_only=True,many=True)
    instructor=UnAuthUserProfileSerializer()
    class Meta:
        model=QaCourses
        fields=['id','pk','title','discountPrice','showDiscountPrice','slug','instructor','theComponents','theReviews','simDesc','fullDesc','youLearn','category','regularPrice','saledPrice','showRegularPrice','itsFree','lessonCounts','dateRegistred','level','houres','status','prevVideo','coverImage','prevImage','instructor','searchKeys']
        depth=3


class InrolledCreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InrolledCourse
        fields='__all__'

class CouponCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CouponCode
        fields='__all__'


class InrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InrolledCourse
        fields='__all__'
        depth=2

class EventEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventEnrolled
        fields='__all__'
        depth=3

class EventEnrolledCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventEnrolled
        fields='__all__'
        


class CourseReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseReview
        fields='__all__'





class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields='__all__'
        depth=1



class AnswerDiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'
class LessonDiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonDiscussion
        fields='__all__'





class UserNotificationsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserNotifications
        fields='__all__'



class LiveEventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LiveEventComment
        fields='__all__'
        depth=1

class LiveEventCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LiveEventComment
        fields='__all__'



class LessonAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'
        depth=1

class LessonAnswersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'

class VoiteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=VoteModel
        fields='__all__'
# class QaCoursesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=QaCourses
#         fields='__all__'