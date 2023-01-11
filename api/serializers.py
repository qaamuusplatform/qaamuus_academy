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

class EventEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventEnrolled
        fields='__all__'
        depth=3



class InrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InrolledCourse
        fields=['theCourse','status','paided','dateInrolled','startDate','endDate','courseProgress','courseProgress','currentLesson','stayedSeconds']
        depth=2


class InrolledSimCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InrolledCourse
        fields=['status','paided','dateInrolled','startDate','endDate','courseProgress','currentLesson','stayedSeconds','itsLatestAccessedCourse']
        depth=2






class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserNotifications
        fields='__all__'
        depth=2




class QaInstructorCourseCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=QaCourses
        fields=['id','pk','title','discountPrice','showDiscountPrice','slug','simDesc','fullDesc','youLearn','category','regularPrice','saledPrice','showRegularPrice','itsFree','lessonCounts','dateRegistred','level','houres','status','prevVideo','coverImage','prevImage','searchKeys']
        depth=3
class QaCourseUserProfileSerializer(serializers.ModelSerializer):
    # persenter=EventViewInstructorSerializer(read_only=True,many=True)
    class Meta:
        model=UserProfile
        fields=['pk','fullName','username','number','aboutMe','summerInfo','userType','profileImage','userTitle','userType']
        depth=2

class InrolledSimCourseSerializer(serializers.ModelSerializer):
    theCourse=QaInstructorCourseCoursesSerializer()
    theUser=QaCourseUserProfileSerializer()
    class Meta:
        model=InrolledCourse
        fields=['status','paided','theCourse','theUser','dateInrolled','startDate','endDate','courseProgress','stayedSeconds',]
        depth=2

class EventViewInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventView
        fields=['pk','id','title','slug','simDesc','desc','prevVideo','image','language','isLiveSdk','level','duration','heroEvent','isPublic','price','itsFree','discountPrice','discountPrice','isLiveIcon','isEnded','eventType','videoUrl','coverImage','dateTimeStarting']
        depth=2

class UserProfileSerializer(serializers.ModelSerializer):
    theCertifications=InstructorCertificationSerializer(read_only=True,many=True)
    theNotifications=UserNotificationsSerializer(read_only=True,many=True)
    enrolledCourses=InrolledCourseSerializer(read_only=True,many=True)
    enrolledEvents=EventEnrolledSerializer(read_only=True,many=True)
    # instructorCourses=QaCoursesSerializer(read_only=True,many=True)
    instructorCourses=QaInstructorCourseCoursesSerializer(read_only=True,many=True)
    persenter=EventViewInstructorSerializer(read_only=True,many=True)
    class Meta:
        model=UserProfile
        fields='__all__'
        depth=2

class UnAuthUserProfileSerializer(serializers.ModelSerializer):
    theCertifications=InstructorCertificationSerializer(read_only=True,many=True)
    enrolledCourses=InrolledCourseSerializer(read_only=True,many=True)
    enrolledEvents=EventEnrolledSerializer(read_only=True,many=True)
    
    instructorCourses=QaInstructorCourseCoursesSerializer(read_only=True,many=True)
    # persenter=EventViewInstructorSerializer(read_only=True,many=True)
    class Meta:
        model=UserProfile
        fields=['pk','fullName','instructorCourses','enrolledCourses','enrolledEvents','username','number','aboutMe','summerInfo','userType','profileImage','userTitle','userType','theCertifications']
        depth=2



class QaCoursesSummerSerializer(serializers.ModelSerializer):
    instructor=QaCourseUserProfileSerializer()
    class Meta:
        model=QaCourses
        fields=['id','pk','title','slug','instructor','simDesc','category','regularPrice','saledPrice','showRegularPrice','itsFree','lessonCounts','dateRegistred','level','houres','status','prevVideo','coverImage','prevImage','searchKeys']
        depth=3



class EventReviewSerializer(serializers.ModelSerializer):
    theUser=QaCourseUserProfileSerializer()
    class Meta:
        model=EventReview
        fields=['pk','id','theEvent','theUser','theText','theRate','dateTime']
        depth=1

class EventViewSerializer(serializers.ModelSerializer):
    theReviews=EventReviewSerializer(read_only=True,many=True)
    persenter=QaCourseUserProfileSerializer()
    class Meta:
        model=EventView
        fields=['pk','id','title','slug','persenter','coHosts','theReviews','simDesc','desc','prevVideo','image','language','meetingId','isLiveSdk','level','duration','heroEvent','isPublic','price','itsFree','discountPrice','discountPrice','isLiveIcon','isEnded','eventType','videoUrl','coverImage','dateTimeStarting']
        depth=2



class OurInterFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OurInterFriends
        fields='__all__'
        depth=1

class EventReviewSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model=EventReview
        fields=['pk','id','theEvent','theText','theRate','dateTime']


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
    theCourse=QaCoursesSummerSerializer()
    theUser=QaCourseUserProfileSerializer()
    class Meta:
        model=CourseReview
        fields=['pk','id','theCourse','theUser','theText','theRate','dateTime']
        depth=1



class QaCoursesSerializer(serializers.ModelSerializer):
    theComponents=lessonCompoSerializer(read_only=True,many=True)
    theReviews=CourseReviewSerializer(read_only=True,many=True)
    instructor=QaCourseUserProfileSerializer()
    class Meta:
        model=QaCourses
        fields=['id','pk','title','discountPrice','showDiscountPrice','slug','instructor','theComponents','theReviews','simDesc','fullDesc','youLearn','category','regularPrice','saledPrice','showRegularPrice','itsFree','lessonCounts','dateRegistred','level','houres','status','prevVideo','coverImage','prevImage','searchKeys']
        depth=3



class InrolledCreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InrolledCourse
        fields='__all__'

class CouponCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CouponCode
        fields='__all__'



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


class ReferralTransactionSerializer(serializers.ModelSerializer):
    theReffUser=QaCourseUserProfileSerializer()
    theInrollement=InrolledSimCourseSerializer()
    class Meta:
        model=ReferralTransaction
        fields=['theReffUser','isReceiving','refMoney','withdrawMoney','theInrollement','status','datetime']
        depth=2
# class QaCoursesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=QaCourses
#         fields='__all__'