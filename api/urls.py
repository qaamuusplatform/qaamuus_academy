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
    path('checkingEmailExist/<str:email>/',views.checkingEmailExist), 
    
    path('jwtAuthToken-user/',views.jwtAuthTokenUser),
    path('jwtAuthToken-login/',views.jwtAuthTokenLogin),



    path('jwt-login/',views.jwtLogin),
    path('jwt-user/',views.jwtUser),
    path('jwt-logout/',views.jwtLogout),
    path('checkUserExistEmailAndUsername/<str:username>/<str:email>/',views.checkUserExistEmailAndUsername), 

    
    # userProfile
    path('userProfile-list/',views.userProfileList),
    path('userProfile-create/',views.userProfileCreate),
    path('userProfile-update/<str:pk>/',views.userProfileUpdate),
    path('userProfile-update-email/<str:email>/',views.userProfileUpdateEmail),
    path('userProfile-delete/<str:pk>/',views.userProfileDelete),
    path('userProfile-detail/<str:pk>/',views.userProfileDetail),
    path('userProfile-detail-username/<str:username>/',views.userProfileDetailUsername),
    path('userEnrollments-detail/<str:pk>/',views.userEnrollmentsDetail),
    path('sendActivationEmailCode/<str:email>/',views.sendActivationEmailCode),



    path('qaEvent-list/',views.qaEventList),
    path('qaEvent-create/',views.qaEventCreate),
    path('qaEvent-update/<str:pk>/',views.qaEventUpdate),
    path('qaEvent-delete/<str:pk>/',views.qaEventDelete),
    path('qaEvent-detail-slug/<str:slug>/',views.qaEventDetailSlug),
    path('qaEvent-detail/<str:pk>/',views.qaEventDetail),

    path('ourInternationalFriends-list/',views.ourInternationalFriendsList),
    path('ourInternationalFriends-create/',views.ourInternationalFriendsCreate),
    path('ourInternationalFriends-update/<str:pk>/',views.ourInternationalFriendsUpdate),
    path('ourInternationalFriends-delete/<str:pk>/',views.ourInternationalFriendsDelete),
    path('ourInternationalFriends-detail/<str:pk>/',views.ourInternationalFriendsDetail),

    
    path('feedBacks-list/',views.feedBacksList),
    path('feedBacks-create/',views.feedBacksCreate),
    path('feedBacks-update/<str:pk>/',views.feedBacksUpdate),
    path('feedBacks-delete/<str:pk>/',views.feedBacksDelete),
    path('feedBacks-detail/<str:pk>/',views.feedBacksDetail),

    # courses
    path('qaCourse-list/',views.qaCoursesList),
    path('qaCourse-create/',views.qaCoursesCreate),
    path('qaCourse-update/<str:pk>/',views.qaCoursesUpdate),
    path('qaCourse-delete/<str:pk>/',views.qaCoursesDelete),
    path('qaCourse-detail/<str:pk>/',views.qaCoursesDetail),
    path('qaCourse-detail-slug/<str:slug>/',views.qaCoursesDetailSlug),

    
    path('lessonComponent-list/',views.lessonsComponentList),
    path('lessonComponent-create/',views.lessonsComponentCreate),
    path('lessonComponent-update/<str:pk>/',views.lessonsComponentUpdate),
    path('lessonComponent-delete/<str:pk>/',views.lessonsComponentDelete),
    path('lessonComponent-detail/<str:pk>/',views.lessonsComponentDetail),
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

    path('eventReview-list/',views.eventReviewList),
    path('eventReview-create/',views.eventReviewCreate),
    path('eventReview-update/<str:pk>/',views.eventReviewUpdate),
    path('eventReview-delete/<str:pk>/',views.eventReviewDelete),
    path('eventReview-detail/<str:pk>/',views.eventReviewDetail),
    
    # courses
    path('discussion-list/',views.discussionList),
    path('this-lesson-discussions-list/<str:pk>/',views.thislessonDiscussionsList),
    path('discussion-create/',views.discussionCreate),
    path('discussion-update/<str:pk>/',views.discussionUpdate),
    path('discussion-delete/<str:pk>/',views.discussionDelete),
    path('discussion-detail/<str:pk>/',views.discussionDetail),
    path('thisUserDiscussions-list/<str:userId>/',views.thisUserDiscussionsList),

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
    path('userNotifications-delete/<str:pk>/',views.userNotificationsDelete),
    path('thisUserNotifications-list/<str:userId>/',views.thisUserNotificationsList),


    
    path('couponCode-list/',views.couponCodeList),
    path('couponCode-create/',views.couponCodeCreate),
    path('couponCode-update/<str:pk>/',views.couponCodeUpdate),
    path('couponCode-detail/<str:pk>/',views.couponCodeDetail),
    path('couponCode-check/<str:couponCode>/',views.couponCodeCheck),
    path('couponCode-delete/<str:pk>/',views.couponCodeDelete),

    
    path('referralTransaction-list/',views.referralTransactionList),
    path('referralTransaction-create/',views.referralTransactionCreate),
    path('referralTransaction-update/<str:pk>/',views.referralTransactionUpdate),
    path('referralTransaction-detail/<str:pk>/',views.referralTransactionDetail),
    path('thisUserReferralTransaction-list/<str:theReffUser>/',views.thisUserReferralTransaction),
    path('referralTransaction-delete/<str:pk>/',views.referralTransactionDelete),

    path('voiteModel-list/',views.voiteModelList),
    path('voiteModel-create/',views.voiteModelCreate),
    path('voiteModel-update/<str:pk>/',views.voiteModelUpdate),
    path('voiteModel-detail/<str:pk>/',views.voiteModelDetail),

     # liveAnswer
    path('lessonAnswers-list/',views.lessonAnswersList),
    path('lessonAnswers-create/',views.lessonAnswersCreate),
    path('lessonAnswers-update/<str:pk>/',views.lessonAnswersUpdate),
    path('lessonAnswers-detail/<str:pk>/',views.lessonAnswersDetail),

    # payment qa
    # path('inroll-course-toUser/<str:usrId>/<str:crsId>/<str:months>/<str:status>/',views.inrollCourseToUser),
    path('inrollCourseToUser/<str:paymentType>/',views.enrollingCourseToUser),
    path('checkWatchThisCourse-slug/<str:usrId>/<str:slug>/',views.checkWatchThisCourseSlug),
    path('checkThisUserInrolledCourse-slug/<str:usrId>/<str:slug>/',views.checkThisUserInrolledCourseSlug),

    
    path('inrollEventToUser/<str:paymentType>/',views.inrollEventToUser),
    path('checkThisUserInrolledEvent/<str:usrId>/<str:evtId>/',views.checkThisUserInrolledEvent),
    path('checkThisUserInrolledEvent-slug/<str:usrId>/<str:slug>/',views.checkThisUserInrolledEventSlug),
    path('enrolledCourseDetail-slug/<str:usrId>/<str:slug>/',views.enrolledCourseDetail),

    

    path('qa-paid-money/<str:payType>/<str:usrNumber>/<str:amount>/<str:crsId>/<str:months>/<str:usrId>/',views.qaPaidMoney),


    # path('getTheSignature/',views.getTheSignature),
    path('qr-send-main/<str:userProfilePK>/',views.qSendMain),
    path('get-current-time/',views.getCurrentTime),

    path('send-reset-password-code/<str:email>/',views.sendResetPasswordCode)
]