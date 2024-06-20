from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import UserProfile,Posts,Comments,Stories



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=UserProfile
        fields="__all__"
        read_only_fields=["id","user","following","block","is_active","created_at","updated_at"]

class CommentSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField(read_only=True)
    user_profile=UserProfileSerializer(read_only=True)
    class Meta:
        model=Comments
        fields="__all__"
        read_only_fields=["id","user","is_active","created_at","updated_at","post",]


class PostSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField() 
    comments=CommentSerializer(many=True,read_only=True)
    user_profile=UserProfileSerializer(read_only=True)
    user_id=serializers.IntegerField(read_only=True)
    
    class Meta:
        model=Posts
        fields="__all__"
        read_only_fields=["id","user","is_active","created_at","updated_at","liked_by",]


class StorySerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Stories
        fields="__all__"
        read_only_fields=["id","user","is_active","created_at","updated_at","expiry_date"]


