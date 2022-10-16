from django.contrib.auth.models import User
from rest_framework import serializers

from a_webinar.models import LiveEventComment

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'

class QaCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=QaCourses
        fields='__all__'

class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseReview
        fields='__all__'
        depth=1

class CourseReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseReview
        fields='__all__'


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lessons
        fields='__all__'
        depth=1


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields='__all__'
        depth=1

class LessonDiscussionSerializer(serializers.ModelSerializer):
    dateSince=serializers.ReadOnlyField(source='date|timesince')
    class Meta:
        model=LessonDiscussion
        fields='__all__'
        depth=1

class LessonDiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonDiscussion
        fields='__all__'

class AnswerDiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'

class AnswerDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonAnswers
        fields='__all__'
        depth=1

class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserNotifications
        fields='__all__'
        depth=1

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