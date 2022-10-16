from django.urls import path
from . import views
urlpatterns = [
    path('',views.qaEvents),
    path('qa-events/',views.qaEvents),
    path('event-detail/<str:pk>/',views.eventDetail),


    # event enrolled
    path('inroll-event-toUser/<str:usrId>/<str:evtId>/<str:status>/',views.inrollEventToUser),

    path('check-this-user-inrolled-event/<str:usrId>/<str:evtId>/',views.checkThisUserInrolledEvent),


]