from api.models import Posts,UserProfile
from rest_framework import serializers
from rest_framework.response import Response


def post_deleted(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        if Posts.objects.filter(id=id):
            post_object=Posts.objects.get(id=id)
            if post_object.is_active==False:
                raise serializers.ValidationError("post does not exist")
            else:
                return fn(request,*args,**kwargs)
        raise serializers.ValidationError("profile does not exist (hard delete)")
    return wrapper

def profile_deleted(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        if UserProfile.objects.filter(id=id):
            profile_object=UserProfile.objects.get(id=id)
            if profile_object.is_active==False:
                raise serializers.ValidationError("profile does not exist")
            else:
                return fn(request,*args,**kwargs)
        raise serializers.ValidationError("profile does not exist (hard delete)")
    return wrapper
    








