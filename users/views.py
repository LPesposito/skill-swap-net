from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import UserProfile, UserSkill


def user_profile_view(request, username: str):
	"""Renderiza o perfil público de um usuário (mesmo comportamento anterior)."""
	User = get_user_model()
	user = get_object_or_404(User, username=username)
	profile = get_object_or_404(UserProfile, user=user)
	offered_skills = UserSkill.objects.filter(user=user)

	avg_rating = 0.0
	if hasattr(user, "get_average_rating"):
		try:
			avg_rating = user.get_average_rating()
		except Exception:
			avg_rating = 0.0

	context = {
		"profile_user": user,
		"profile": profile,
		"offered_skills": offered_skills,
		"average_rating": avg_rating,
	}

	return render(request, "users/profile.html", context)


class UserSkillListView(ListView):
	model = UserSkill
	template_name = "users/skill_list.html"
	context_object_name = "skills"

	def get_queryset(self):
		return UserSkill.objects.filter(user=self.request.user)


class UserSkillCreateView(LoginRequiredMixin, CreateView):
	model = UserSkill
	fields = ["name", "description"]
	template_name = "users/skill_form.html"
	success_url = reverse_lazy("users:skill_list")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class UserSkillUpdateView(LoginRequiredMixin, UpdateView):
	model = UserSkill
	fields = ["name", "description"]
	template_name = "users/skill_form.html"
	success_url = reverse_lazy("users:skill_list")

	def get_queryset(self):
		return UserSkill.objects.filter(user=self.request.user)


class UserSkillDeleteView(LoginRequiredMixin, DeleteView):
	model = UserSkill
	template_name = "users/skill_confirm_delete.html"
	success_url = reverse_lazy("users:skill_list")

	def get_queryset(self):
		return UserSkill.objects.filter(user=self.request.user)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = UserProfile
	fields = ["bio", "location"]
	template_name = "users/profile_edit.html"
	success_url = reverse_lazy("users:profile_edit")

	def get_object(self, queryset=None):
		# Allow users to edit only their own profile
		return get_object_or_404(UserProfile, user=self.request.user)
