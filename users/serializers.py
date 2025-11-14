from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import UserProfile, UserSkill

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "bio", "location", "created_at")


class UserSkillSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = ("id", "user", "name", "description", "created_at")
