from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .models import UserProfile, UserSkill
from .serializers import UserProfileSerializer, UserSkillSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any, write only for owner (user/profile/skill owner)
        if request.method in permissions.SAFE_METHODS:
            return True
        # obj may be UserProfile or UserSkill
        owner = getattr(obj, "user", None)
        return owner == request.user


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Attach the logged user if possible
        serializer.save(user=self.request.user)


class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.select_related("user").all()
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request):
        qs = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
