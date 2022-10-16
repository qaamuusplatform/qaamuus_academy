from datetime import timedelta,datetime
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
# Create your models here.


class UserTypes(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self) -> str:
        return str(self.name)

class SearchKeys(models.Model):
    searchName=models.CharField(max_length=1000)
    simDesc=models.TextField()
    fullDesc=models.TextField()

    def __str__(self) -> str:
        return str(self.searchName)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    number=models.CharField(max_length=16, default=0)
    profileImage=models.ImageField(upload_to='images/usrProfile',null=True,blank=True)
    password=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    userTitle=models.CharField(max_length=255,null=True,blank=True)
    fullName=models.CharField(max_length=255)
    aboutMe=models.TextField(null=True,blank=True)
    stayedSeconds=models.IntegerField(default=0)
    facebook_link=models.CharField(max_length=3000,null=True,blank=True)
    twitter_link=models.CharField(max_length=3000,null=True,blank=True)
    third_link=models.CharField(max_length=3000,null=True,blank=True)
    # followedUsers=models.ManyToManyField()
    learnedSeconds=models.IntegerField(default=0)
    status=models.BooleanField(default=True)
    contactMe=models.TextField(null=True,blank=True)
    userType=models.ForeignKey(UserTypes,on_delete=models.CASCADE,default=1)
    teacherPoints=models.FloatField(default=1)
    user_activated=models.BooleanField(default=True)
    def theImage(self):
        return mark_safe('<img src={} width="100px" >'.format(self.profileImage.url))
    theImage.allow_tags=True
    def __str__(self) -> str:
        return str(self.fullName )+' -- '+str(self.number)

class InstructorCertification(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    certificateName=models.CharField(max_length=255)
    certificateDesc=models.CharField(max_length=2655)
    certificateDate=models.DateField()
    def __str__(self) -> str:
        return str(self.theUser.fullName )+' -- '+str(self.certificateName)




class CourseCategory(models.Model):
    categoryName=models.CharField(max_length=255)
    categoryDesc=models.TextField(default='')
    categoryImage=models.ImageField(upload_to='images/category/',null=True,blank=True)
    courses=models.IntegerField(default=1)
    def theCategoryImage(self):
        return mark_safe('<img src={} width="100px" >'.format(self.categoryImage.url))
    theCategoryImage.allow_tags=True
    def __str__(self) -> str:
        return str(self.categoryName)


class QaCourses(models.Model):
    title=models.CharField(max_length=255)
    simDesc=models.TextField(null=True,blank=True)
    fullDesc=RichTextField()
    youLearn=RichTextField(null=True,blank=True)
    category=models.ForeignKey(CourseCategory,on_delete=models.CASCADE,null=True,blank=True)
    inrolledUsers=models.ManyToManyField(UserProfile,'inrolledU',null=True,blank=True)
    regularPrice=models.FloatField(default=0)
    showRegularPrice=models.BooleanField(default=True)
    saledPrice=models.FloatField(default=0)
    lessonCounts=models.IntegerField(default=0)
    itsFree=models.BooleanField(default=False)
    dateRegistred=models.DateField(auto_now=True)
    level=models.CharField(max_length=255,default='Standared')
    houres=models.CharField(max_length=255,default='0')
    status=models.BooleanField(default=True)
    prevVideo=models.CharField(max_length=255000)
    coverImage=models.ImageField(upload_to='images/courseImages/',blank=True,null=True)
    prevImage=models.ImageField(upload_to='images/courseImages/')
    instructor=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    searchKey=models.ManyToManyField(SearchKeys,blank=True,null=True)

    

    def courPrevIg(self):
        return mark_safe('<img src={} width="100px" >'.format(self.prevImage.url))
    courPrevIg.allow_tags=True

    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.instructor)


class lessonCompo(models.Model):
    compoName=models.CharField(max_length=255,default='')
    theCourse=models.ForeignKey(QaCourses,on_delete=models.CASCADE,default=1)
    def __str__(self) -> str:
        return str(self.compoName)+' -- '+str(self.theCourse)


class Lessons(models.Model):
    title=models.CharField(max_length=255)  
    lessonNum=models.IntegerField(default=1)
    theCourse=models.ForeignKey(QaCourses,on_delete=models.CASCADE)
    simDesc=models.TextField(null=True,blank=True)
    compo=models.ForeignKey(lessonCompo,on_delete=models.CASCADE,default=1)
    fullDesc=RichTextField()
    lessonVideo=models.FileField(upload_to='videos/lessons/',null=True,blank=True)
    lessonLink=models.CharField(max_length=3000,null=True,blank=True)
    dateRegistred=models.DateField(auto_now=True)
    duration=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.theCourse.title)


class LessonDiscussion(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theLesson=models.ForeignKey(Lessons,on_delete=models.CASCADE)
    discText=models.TextField()
    theAnswers=models.IntegerField(default=0)
    date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.theUser.fullName) + '--' +str(self.theLesson) 

class LessonAnswers(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theDiscussion=models.ForeignKey(LessonDiscussion,on_delete=models.CASCADE)
    ansText=RichTextField()
    likedTheAnswer=models.ManyToManyField(UserProfile,related_name='likedUsers',null=True,blank=True)
    date=models.DateTimeField(auto_now=True)

class FeedBacks(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    stars=models.IntegerField(default=3)
    date=models.DateField(auto_now=True)
    fText=models.TextField()
    isActive=models.BooleanField(default=False)

    def userImage(self):
        return mark_safe('<img src={} width="100px" >'.format(self.theUser.profileImage.url))
    userImage.allow_tags=True

    # def __str__(self) -> str:
    #     return str(self.theUser.fullName)+' -- '+str(self.stars)


class Topic(models.Model):
    title=models.CharField(max_length=255)
    theLesson=models.ForeignKey(Lessons,on_delete=models.CASCADE)
    dateRegistred=models.DateField(auto_now=True)
    fullDesc=RichTextField()

    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.theLesson.title)

class UserNotifications(models.Model):
    toUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    seen=models.BooleanField(default=False)
    fromUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='sender')
    text=models.TextField(default='')
    dateTime=models.DateTimeField(auto_now=True)

def one_month_from_today():
    return datetime.now() + timedelta(days=30)
    
class InrolledCourse(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theCourse=models.ForeignKey(QaCourses,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    dateInrolled=models.DateTimeField(auto_now=True)
    startDate=models.DateTimeField(auto_now=True)
    endDate=models.DateField(default=one_month_from_today)
    courseProgress=models.FloatField(default=0)
    currentLesson=models.ForeignKey(Lessons,on_delete=models.CASCADE,null=True,blank=True)
    stayedSeconds=models.CharField(max_length=255)
    itsLatestAccessedCourse=models.BooleanField(default=False)


class CourseReview(models.Model):
    theCourse=models.ForeignKey(QaCourses,on_delete=models.CASCADE)
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theText=models.TextField(default='')
    theRate=models.IntegerField(default=3)
    dateTime=models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return str(self.theCourse.title)+' -- '+str(self.theUser.fullName)+' -- '+str(self.theRate)

class PaymentReport(models.Model):
    theInrolledCourse=models.ForeignKey(InrolledCourse,on_delete=models.CASCADE)
