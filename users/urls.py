from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Profile page by username
    path("profile/<str:username>/", views.user_profile_view, name="user_profile"),
]

# API routes (DRF)
from rest_framework.routers import DefaultRouter
from . import api
from django.urls import include

router = DefaultRouter()
router.register(r"profiles", api.UserProfileViewSet, basename="profile")
router.register(r"skills", api.UserSkillViewSet, basename="skills")

urlpatterns += [
    path("api/", include((router.urls, "users-api"))),
]

# Basic CRUD UI for skills and profile edits
urlpatterns += [
    path("skills/", views.UserSkillListView.as_view(), name="skill_list"),
    path("skills/add/", views.UserSkillCreateView.as_view(), name="skill_add"),
    path("skills/<int:pk>/edit/", views.UserSkillUpdateView.as_view(), name="skill_edit"),
    path("skills/<int:pk>/delete/", views.UserSkillDeleteView.as_view(), name="skill_delete"),
    path("profile/<str:username>/edit/", views.UserProfileUpdateView.as_view(), name="profile_edit"),
]
