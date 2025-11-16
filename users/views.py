from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import UserProfile, UserSkill


def user_profile_view(request, username: str):
	"""Renderiza o perfil público de um usuário (mesmo comportamento anterior)."""
	User = get_user_model()
	user = get_object_or_404(User, username=username)
	# Garantir que o perfil exista mesmo para contas antigas/criadas fora do fluxo de signup
	profile, _ = UserProfile.objects.get_or_create(user=user)
	offered_skills = UserSkill.objects.filter(user=user)

	# Optional: recent requests created by this user (as "requested" skills)
	try:
		from services.models import ServiceRequest

		recent_requests = (
			ServiceRequest.objects.filter(requester=user)
			.select_related("offered_skill", "provider")
			.order_by("-created_at")[:5]
		)
	except Exception:
		recent_requests = []

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
		"recent_requests": recent_requests,
	}

	return render(request, "users/profile.html", context)


def signup_view(request):
	"""Simple user signup using Django's UserCreationForm."""
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Ensure a profile exists
			UserProfile.objects.get_or_create(user=user)
			# Auto-login and redirect to profile edit
			username = form.cleaned_data.get("username")
			raw_password = form.cleaned_data.get("password1")
			auth_user = authenticate(request, username=username, password=raw_password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("users:profile_edit", username=auth_user.username)
			messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
			return redirect("login")
	else:
		form = UserCreationForm()

	return render(request, "registration/register.html", {"form": form})


    


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
	fields = ["display_name", "bio", "location"]
	template_name = "users/profile_edit.html"
	success_url = None

	def get_object(self, queryset=None):
		# Allow users to edit only their own profile, create if missing
		obj, _ = UserProfile.objects.get_or_create(user=self.request.user)
		return obj

	def get_success_url(self):
		return reverse_lazy("users:profile_edit", kwargs={"username": self.request.user.username})
