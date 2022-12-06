from django.contrib import admin
from . models import *
from  api.models import VoteModel 
# Register your models heree.
admin.site.register(OurInterFriends)
admin.site.register(AboutQaamuusInfo)
admin.site.register(VoteModel)
