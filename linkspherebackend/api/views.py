from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework import serializers
from rest_framework.decorators import action

from api.serializers import UserSerializer,UserProfileSerializer,PostSerializer,CommentSerializer,StorySerializer
from api.models import UserProfile,Posts,Comments,Stories
from api.decorators import post_deleted ,profile_deleted

# Create your views here.

class SignUpView(APIView):
    
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
        
class UserProfileView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserProfileSerializer
    queryset=UserProfile.objects.filter(is_active=True)
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def perform_update(self, serializer):
        id=self.kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        if profile_object.user != self.request.user:
            raise serializers.ValidationError("permission denied")
        return super().perform_update(serializer)
    
    @method_decorator(profile_deleted)
    @action(methods=["get"],detail=True)
    def follow(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        if profile_object in request.user.profile.following.all():
            request.user.profile.following.remove(profile_object)
            return Response(data={"unfollowed"})
        request.user.profile.following.add(profile_object)
        return Response(data={"followed"})
    
    @method_decorator(profile_deleted)
    @action(methods=["get"],detail=True)
    def block(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        if profile_object in request.user.profile.block.all():
            request.user.profile.block.remove(profile_object)
            return Response(data={"unblocked"})
        request.user.profile.block.add(profile_object)
        return Response(data={"blocked"})
    

class PostView(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.filter(is_active=True).order_by("-created_at")
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    @method_decorator(post_deleted)
    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        if post_object.user != request.user:
            raise serializers.ValidationError("permission denied")
        Posts.objects.filter(id=id).update(is_active=False)
        return Response(data={"post was deleted"})
    
    @method_decorator(post_deleted)
    @action(methods=["get"],detail=True)
    def like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        if request.user not in post_object.liked_by.all():
            post_object.liked_by.add(request.user)
            return Response(data={"liked"})
        post_object.liked_by.remove(request.user)
        return Response(data={"disliked"})
    
    @method_decorator(post_deleted)
    @action(methods=["post"],detail=True)
    def comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,post=post_object)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    

class CommentDeleteView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        comment_object=Comments.objects.filter(id=id)
        if comment_object:
            comment_object=Comments.objects.get(id=id)
            if comment_object.user != request.user:
                raise serializers.ValidationError("permission denied")
            elif comment_object.is_active==False:
                raise serializers.ValidationError("comment does not exist")
            else:
                Comments.objects.filter(id=id).update(is_active=False)
                return Response(data={"deleted"})
        raise serializers.ValidationError("comment does not exist (hard delete)")

        
class StoryView(viewsets.ModelViewSet):
    serializer_class=StorySerializer
    queryset=Stories.objects.filter(is_active=True,expiry_date__gt=timezone.now())
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        story_object=Stories.objects.filter(id=id)
        if story_object:
            story_object=Stories.objects.get(id=id)
            if story_object.user != request.user:
                raise serializers.ValidationError("permission denied")
            elif story_object.is_active==False:
                raise serializers.ValidationError("story does'nt exist")     
            else:
                Stories.objects.filter(id=id).update(is_active=False)
        raise serializers.ValidationError("story does not exist (hard delete)")

class UserDetailView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        data={}
        data["user_id"]=request.user.id
        data["username"]=request.user.username
        data["profile_id"]=request.user.profile.id
        return Response(data=data)



