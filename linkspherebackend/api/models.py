# import from django

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone 
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(upload_to="profilepics",null=True,blank=True,default="profilepics/default.png")
    dob=models.DateField(null=True)
    bio=models.CharField(max_length=200,null=True)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False)
    block=models.ManyToManyField("self",related_name="blocked",symmetrical=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userpost")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="posters",null=True,blank=True)
    liked_by=models.ManyToManyField(User,related_name="post_like",blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


    @property
    def comments(self):
        return self.post_comments.all()
    
    @property
    def user_profile(self):
        return self.user.profile

    def __str__(self):
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    post=models.ForeignKey(Posts,related_name="post_comments",on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

    @property
    def user_profile(self):
        return self.user.profile


    def __str__(self):
        return self.text


class Stories(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userstories")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="stories",null=True,blank=True)
    expiry_date=models.DateTimeField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    # exp=created_date + timezone.timedelta(days=1)


    def __str__(self):
        return self.title 
    
    def save(self,*args,**kwargs):
        self.expiry_date=timezone.now()+timezone.timedelta(days=1)
        super().save(*args,**kwargs)
    

def create_profile(sender,created,instance,**kwargs):

    if created:
        UserProfile.objects.create(user=instance)
         


post_save.connect(create_profile,sender=User)