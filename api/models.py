from datetime import timedelta,datetime
from email.policy import default
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import random
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
    username=models.CharField(max_length=255,default='')
    email=models.CharField(max_length=255,unique=True)
    userTitle=models.CharField(max_length=255,null=True,blank=True)
    
    fullName=models.CharField(max_length=255)
    aboutMe=RichTextField(null=True,blank=True)
    stayedSeconds=models.IntegerField(default=0)
    facebook_link=models.CharField(max_length=3000,null=True,blank=True)
    twitter_link=models.CharField(max_length=3000,null=True,blank=True)
    third_link=models.CharField(max_length=3000,null=True,blank=True)
    # followedUsers=models.ManyToManyField()
    learnedSeconds=models.IntegerField(default=0)
    city=models.CharField(default='',null=True,blank=True,max_length=255)
    status=models.BooleanField(default=True)
    contactMe=models.TextField(null=True,blank=True)
    referralCode=models.CharField(default='qReff_9002',max_length=10)
    userType=models.ForeignKey(UserTypes,on_delete=models.CASCADE,default=1)
    teacherPoints=models.FloatField(default=1)
    user_activated=models.BooleanField(default=True)

    # def save(self,*args,**kwargs):
    #     if self._state.adding:
    #         self.referralCode=generateRandomReffralCode()
    def theImage(self):
        if self.profileImage:
            return mark_safe('<img src={} width="100px" >'.format(self.profileImage.url))
        else:
            return mark_safe('<img src={} width="100px" >'.format('https://st3.depositphotos.com/3581215/18899/v/450/depositphotos_188994514-stock-illustration-vector-illustration-male-silhouette-profile.jpg')) 
    theImage.allow_tags=True
    def __str__(self) -> str:
        return str(self.fullName )+' -- '+str(self.number)

class InstructorCertification(models.Model):
    theUser=models.ForeignKey(UserProfile,related_name='theCertifications',on_delete=models.CASCADE)
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
    slug=models.CharField(max_length=2555,default='')
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
    hasCertificate=models.BooleanField(default=False)
    dateRegistred=models.DateField(auto_now=True)
    level=models.CharField(max_length=255,default='Standared')
    language=models.CharField(max_length=255,default='Somali')
    houres=models.CharField(max_length=255,default='0')
    status=models.BooleanField(default=True)
    prevVideo=models.CharField(max_length=255000)
    coverImage=models.ImageField(upload_to='images/courseImages/',blank=True,null=True)
    prevImage=models.ImageField(upload_to='images/courseImages/')
    instructor=models.ForeignKey(UserProfile,related_name='instructor',on_delete=models.CASCADE)
    searchKeys=models.ManyToManyField(SearchKeys,blank=True,null=True)
    # relatedCourses=models.ManyToManyField(QaCourses,blank=True,null=True)

    def save(self,*args,**kwargs):
        self.slug = self.title.replace(' ','-').casefold()
        # self.save()
        return super().save()

    def courPrevIg(self):
        return mark_safe('<img src={} width="100px" >'.format(self.prevImage.url))
    courPrevIg.allow_tags=True

    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.instructor)

class CouponCode(models.Model):
    couponCode=models.CharField(max_length=255,default='')
    expireDate=models.DateField(default=datetime.now() + timedelta(days=2))
    discountPrice=models.FloatField(default=5)

    def __str__(self) -> str:
        return str(self.couponCode)+' -- '+str(self.discountPrice)+' -- '+str(self.expireDate)


class lessonCompo(models.Model):
    compoName=models.CharField(max_length=255,default='')
    orderNum=models.IntegerField(default=0)
    lessonsCount=models.IntegerField(default=1)
    totalHours=models.CharField(default='30:00',max_length=10)
    simDesc=models.TextField(default='')
    theCourse=models.ForeignKey(QaCourses,related_name='theComponents',on_delete=models.CASCADE,default=1)
    
    class Meta:
        ordering = ['orderNum']
    def __str__(self) -> str:
        return str(self.compoName)+' -- '+str(self.theCourse)


class Lessons(models.Model):
    title=models.CharField(max_length=255)  
    lessonNum=models.IntegerField(default=1)
    theCourse=models.ForeignKey(QaCourses,related_name='theLessons',on_delete=models.CASCADE)
    simDesc=models.TextField(null=True,blank=True)
    compo=models.ForeignKey(lessonCompo,related_name='theCompoLessons',on_delete=models.CASCADE,default=1)
    fullDesc=RichTextField()
    lessonVideo=models.FileField(upload_to='videos/lessons/',null=True,blank=True)
    lessonLink=models.CharField(max_length=3000,null=True,blank=True)
    dateRegistred=models.DateField(auto_now=True)
    duration=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.theCourse.title)

    def save(self,*args,**kwargs):
        self.compo.lessonsCount=Lessons.objects.filter(compo=self.compo).count()
        self.save()
        return super().save()


class LessonDiscussion(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theLesson=models.ForeignKey(Lessons,related_name='theDiscussions',on_delete=models.CASCADE)
    discText=models.TextField()
    theAnswers=models.IntegerField(default=0)
    date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.theUser.fullName) + '--' +str(self.theLesson) 

class LessonAnswers(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theDiscussion=models.ForeignKey(LessonDiscussion,related_name='theDiscussionAnswers',on_delete=models.CASCADE)
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
    toUser=models.ForeignKey(UserProfile,related_name='theNotifications',on_delete=models.CASCADE)
    seen=models.BooleanField(default=False)
    title=models.CharField(default='',max_length=255,null=True,blank=True)
    fromUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='sender')
    text=models.TextField(default='')
    dateTime=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['seen']
    
    def __str__(self) -> str:
        return str(self.title)+' -- '+str(self.seen)

def one_month_from_today():
    return datetime.now() + timedelta(days=30)
    
class InrolledCourse(models.Model):
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theCourse=models.ForeignKey(QaCourses,on_delete=models.CASCADE)
    referralCode=models.CharField(null=True,blank=True,max_length=255)
    cupponCode=models.CharField(null=True,blank=True,max_length=255)
    status=models.BooleanField(default=False)
    dateInrolled=models.DateTimeField(auto_now=True)
    startDate=models.DateTimeField(auto_now=True)
    endDate=models.DateField(default=one_month_from_today)
    courseProgress=models.FloatField(default=0)
    currentLesson=models.ForeignKey(Lessons,on_delete=models.CASCADE,null=True,blank=True)
    stayedSeconds=models.CharField(max_length=255)
    itsLatestAccessedCourse=models.BooleanField(default=False)


class CourseReview(models.Model):
    theCourse=models.ForeignKey(QaCourses,related_name='theReviews',on_delete=models.CASCADE)
    theUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    theText=models.TextField(default='')
    theRate=models.IntegerField(default=3)
    dateTime=models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return str(self.theCourse.title)+' -- '+str(self.theUser.fullName)+' -- '+str(self.theRate)

class PaymentReport(models.Model):
    theInrolledCourse=models.ForeignKey(InrolledCourse,on_delete=models.CASCADE)








class VoteModel(models.Model):
    magaca=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    phoneNumber =models.CharField(max_length=255)
    qaabkaWaxbarashada=models.CharField(max_length=255)
    maadadaAadDaneeneeso =models.CharField(max_length=255)
    waqtiga =models.CharField(max_length=255,default='')
    macalimiinta =models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.magaca) +' -- '+str(self.phoneNumber)



