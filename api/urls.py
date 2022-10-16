from django.urls import path
from . import views
urlpatterns = [
    # user request
    path('user-list/',views.userList),
    path('user-create/',views.userCreate),
    path('user-update/<str:pk>/',views.userUpdate),
    path('user-delete/<str:pk>/',views.userDelete),
    path('user-detail/<str:pk>/',views.userDetail),
    path('user-password-format/<str:pk>/',views.passwordFormat),
    path('checkingUserExist/<str:username>/',views.checkingUserExist), 

    
    # userProfile
    path('userProfile-list/',views.userProfileList),
    path('userProfile-create/',views.userProfileCreate),
    path('userProfile-update/<str:pk>/',views.userProfileUpdate),
    path('userProfile-delete/<str:pk>/',views.userProfileDelete),
    path('userProfile-detail/<str:pk>/',views.userProfileDetail),


    # courses
    path('qaCourse-list/',views.qaCoursesList),
    path('qaCourse-create/',views.qaCoursesCreate),
    path('qaCourse-update/<str:pk>/',views.qaCoursesUpdate),
    path('qaCourse-delete/<str:pk>/',views.qaCoursesDelete),
    path('qaCourse-detail/<str:pk>/',views.qaCoursesDetail),

     # lessons
    path('lesson-list/',views.lessonList),
    path('this-course-lessons-list/<str:pk>/',views.thisCourseLessonList),
    path('lesson-create/',views.lessonCreate),
    path('lesson-update/<str:pk>/',views.lessonUpdate),
    path('lesson-delete/<str:pk>/',views.lessonDelete),
    path('lesson-detail/<str:pk>/',views.lessonDetail),


    # topics
    path('topic-list/',views.topicList),
    path('this-lesson-topics-list/<str:pk>/',views.thislessonTopicsList),
    path('topic-create/',views.topicCreate),
    path('topic-update/<str:pk>/',views.topicUpdate),
    path('topic-delete/<str:pk>/',views.topicDelete),
    path('topic-detail/<str:pk>/',views.topicDetail),

    # courses
    path('courseReview-list/',views.courseReviewList),
    path('this-course-CourseReview-list/<str:pk>/',views.thisCourseReviewList),
    path('courseReview-create/',views.courseReviewCreate),
    path('courseReview-update/<str:pk>/',views.courseReviewUpdate),
    path('courseReview-delete/<str:pk>/',views.courseReviewDelete),
    path('courseReview-detail/<str:pk>/',views.courseReviewDetail),
    
    # courses
    path('discussion-list/',views.discussionList),
    path('this-lesson-discussions-list/<str:pk>/',views.thislessonDiscussionsList),
    path('discussion-create/',views.discussionCreate),
    path('discussion-update/<str:pk>/',views.discussionUpdate),
    path('discussion-delete/<str:pk>/',views.discussionDelete),
    path('discussion-detail/<str:pk>/',views.discussionDetail),

     # comment
    path('liveEventComment-list/',views.liveEventCommentList),
    path('this-event-liveEventComment-list/<str:pk>/',views.thisEventLiveEventCommentList),
    path('liveEventComment-create/',views.liveEventCommentCreate),
    path('liveEventComment-update/<str:pk>/',views.liveEventCommentUpdate),
    path('liveEventComment-delete/<str:pk>/',views.liveEventCommentDelete),
    path('liveEventComment-detail/<str:pk>/',views.liveEventCommentDetail),
    
    # notificaiton
    path('userNotifications-list/',views.userNotificationsList),
    path('userNotifications-create/',views.userNotificationsCreate),
    path('userNotifications-update/<str:pk>/',views.userNotificationsUpdate),
    path('userNotifications-detail/<str:pk>/',views.userNotificationsDetail),

     # liveAnswer
    path('lessonAnswers-list/',views.lessonAnswersList),
    path('lessonAnswers-create/',views.lessonAnswersCreate),
    path('lessonAnswers-update/<str:pk>/',views.lessonAnswersUpdate),
    path('lessonAnswers-detail/<str:pk>/',views.lessonAnswersDetail),

    # payment qa
    path('inroll-course-toUser/<str:usrId>/<str:crsId>/<str:months>/<str:status>/',views.inrollCourseToUser),
    path('qa-paid-money/<str:payType>/<str:usrNumber>/<str:amount>/<str:crsId>/<str:months>/<str:usrId>/',views.qaPaidMoney),


    # path('getTheSignature/',views.getTheSignature),
    path('qr-send-main/<str:userProfilePK>/',views.qSendMain),
    path('get-current-time/',views.getCurrentTime),

    path('send-reset-password-code/<str:username>/',views.sendResetPasswordCode)
]