from django.urls import path

from . import views

# from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.indexWeb),

    path('qa-courses/',views.qaCourses),
    path('qa-courses/<str:categoryPk>/',views.qaCoursesCategory),
    path('crs-dtl-wth/<str:pk>/<str:encTitle>/',views.crsDtlWth),
    path('my-courses/<str:pk>/<str:encTitle>/',views.myCourses),
    path('pymt-thcr/<str:searchKey>/<str:pk>/<str:encTitle>/',views.paymentPage),

    # inrollment
    path('course-tk/inrolled/lssn-tpc/<str:crsPk>/<str:encTitle>/<str:lessonId>/',views.courseTakeInrolledLesson),
    path('discussion-detail/<str:discId>/',views.discussionDetail),
    path('live-the-answer/<str:answId>/<str:userId>/<str:discId>/',views.liveTheAnswer),


    # events
    path('events/',views.events),
    path('event-detail/<str:pk>/<str:enc1>/',views.eventDetail),
    path('event-commin-timer/<str:enc1>/<str:evtId>/<str:enc2>/',views.eventComminTimer),
    path('webinar/v-live/<str:evtId>/<str:evtTitle>/',views.webinarLive),


    # aboutuser
    path('sing-in/',views.singIn),
    path("instroctor-info/<str:usrId>/<str:enc1>/",views.instroctorInfo),
    path('user-dash/<str:enc1>/<str:usrId>/<str:enc2>/',views.usrDashboard),
    path('user-edit/<str:enc1>/<str:usrId>/<str:enc2>/',views.usrEdit),
    path('register-nu/',views.registerNu),
    path('logout/',views.logouThisUser),

    
    # members
    path('instructors/',views.instructor),
    # path('instructors/',views.instructor),

    # email active code
    path('send-activation-email-link/<str:usrId>/',views.sendActivationEmail),
    path('email/activation/<str:usrId>/<int:timeAsMap>/',views.activateEmail),


    # reset email password
    path('password-reset/',views.passwordReset),
    path('create/new-password/<str:usrId>/',views.createNewPassword),

    # path('live/preparing/',views.livePreparing),
    path('webinar/live/<str:theEventPk>/preparing/',views.livePreparing),
    path('webinar/live/meeting/<str:evtId>',views.webinarLiveMeeting),



    path('register-your-vote/',views.voteScreen)

]

