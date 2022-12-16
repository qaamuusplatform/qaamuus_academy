from django.contrib import admin
from . models import *
# Register your admin sites m.
admin.site.register(UserTypes)
# admin.site.register(UserProfile)
admin.site.register(CouponCode)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('fullName','theImage','user','userType','number','email','status')
    # ordering: 
    search_fields=('fullName','number','email','status')
admin.site.register(InstructorCertification)
    
@admin.register(QaCourses)
class QaCoursesAdmin(admin.ModelAdmin):
    list_display=('title','courPrevIg','simDesc','instructor','regularPrice','saledPrice','itsFree','status','dateRegistred')
    # ordering: 
    search_fields=('title','simDesc','instructor')

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display=('title','theCourse','lessonNum','dateRegistred')
    # ordering: 
    search_fields=('title','dateRegistred')


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display=('categoryName','theCategoryImage')
    # ordering: 
    search_fields=('pk','categoryName')

@admin.register(FeedBacks)
class FeedBacksAdmin(admin.ModelAdmin):
    list_display=('theUser','stars','date','fText','isActive')
    # ordering: 
    search_fields=('pk','theUser','stars','fText','isActive')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display=('title','theLesson','dateRegistred')
    search_fields=('pk','theLesson','title','dateRegistred')

admin.site.register(lessonCompo)
# admin.site.register(SearchKeys)

admin.site.register(LessonDiscussion)
@admin.register(InrolledCourse)
class InrolledCourseAdmin(admin.ModelAdmin):
    list_display=('theCourse','theUser','courseProgress','status')
    # ordering=('-dateInrolled')
    search_fields=('pk','theUser__fullName','theUser__number','theUser__email','startDate')
