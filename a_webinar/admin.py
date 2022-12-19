
from django.contrib import admin
from .models import *
# Register your hee.

admin.site.register(EventView)
admin.site.register(EventReview)
# admin.site.register(EventEnrolled)

@admin.register(EventEnrolled)
class EventEnrolledAdmin(admin.ModelAdmin):
    list_display=('theUser','pk','theEvent','paided','dateTr')
    # ordering: 
    search_fields=('pk','dateTr')
