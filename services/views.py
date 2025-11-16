from django.db.models import Q, Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView

from .models import ServiceRequest
from .forms import ServiceRequestForm


def feed_view(request):
	q = (request.GET.get("q") or "").strip()

	qs = (
		ServiceRequest.objects.select_related("offered_skill", "provider", "provider__profile")
		.annotate(avg_rating=Avg("provider__reviews_received__rating"))
		.order_by("-created_at")
	)

	if q:
		qs = qs.filter(
			Q(offered_skill__name__icontains=q)
			| Q(description__icontains=q)
			| Q(provider__username__icontains=q)
			| Q(provider__profile__location__icontains=q)
			| Q(requester__username__icontains=q)
		)

	context = {
		"services": qs,
		"q": q,
	}
	return render(request, "services/feed.html", context)


class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
	model = ServiceRequest
	form_class = ServiceRequestForm
	template_name = "services/request_form.html"
	success_url = reverse_lazy("services:requests")

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["request"] = self.request
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		skill_id = self.request.GET.get("skill")
		if skill_id:
			initial["offered_skill"] = skill_id
		return initial

	def form_valid(self, form):
		form.instance.requester = self.request.user
		form.instance.provider = form.cleaned_data["offered_skill"].user
		return super().form_valid(form)


class MyRequestsListView(LoginRequiredMixin, ListView):
	model = ServiceRequest
	template_name = "services/my_requests.html"
	context_object_name = "requests"

	def get_queryset(self):
		return (
			ServiceRequest.objects.select_related("offered_skill", "provider", "provider__profile")
			.filter(requester=self.request.user)
			.order_by("-created_at")
		)


class MyOffersListView(LoginRequiredMixin, ListView):
	model = ServiceRequest
	template_name = "services/my_offers.html"
	context_object_name = "offers"

	def get_queryset(self):
		return (
			ServiceRequest.objects.select_related("offered_skill", "requester", "requester__profile")
			.filter(provider=self.request.user)
			.order_by("-created_at")
		)


from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


@require_POST
def update_request_status(request, pk: int):
	if not request.user.is_authenticated:
		return redirect("login")

	sr = get_object_or_404(ServiceRequest, pk=pk)
	action = request.POST.get("action")

	allowed = False
	if action == "accept" and request.user == sr.provider and sr.status == ServiceRequest.Status.PENDING:
		sr.status = ServiceRequest.Status.ACCEPTED
		allowed = True
	elif action == "complete" and request.user == sr.provider and sr.status == ServiceRequest.Status.ACCEPTED:
		sr.status = ServiceRequest.Status.COMPLETED
		allowed = True
	elif action == "cancel" and (request.user == sr.provider or request.user == sr.requester) and sr.status in (
		ServiceRequest.Status.PENDING,
		ServiceRequest.Status.ACCEPTED,
	):
		sr.status = ServiceRequest.Status.CANCELED
		allowed = True

	if allowed:
		sr.save(update_fields=["status"])
		messages.success(request, "Status atualizado.")
	else:
		messages.error(request, "Ação não permitida.")

	next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("services:feed")
	return redirect(next_url)
