from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class ServiceRequest(models.Model):
	class Status(models.TextChoices):
		PENDING = "PENDING", "Pending"
		ACCEPTED = "ACCEPTED", "Accepted"
		COMPLETED = "COMPLETED", "Completed"
		CANCELED = "CANCELED", "Canceled"

	requester = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="service_requests_made",
		on_delete=models.CASCADE,
	)
	provider = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="service_requests_received",
		on_delete=models.CASCADE,
	)
	# Referência por string para evitar import circular com app `users`
	offered_skill = models.ForeignKey("users.UserSkill", related_name="service_requests", on_delete=models.CASCADE)
	description = models.TextField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"ServiceRequest(id={self.id}, requester={self.requester}, provider={self.provider}, status={self.status})"


class Review(models.Model):
	RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

	transaction = models.OneToOneField(
		ServiceRequest, related_name="review", on_delete=models.CASCADE
	)
	reviewer = models.ForeignKey(
		settings.AUTH_USER_MODEL, related_name="reviews_made", on_delete=models.CASCADE
	)
	reviewed_user = models.ForeignKey(
		settings.AUTH_USER_MODEL, related_name="reviews_received", on_delete=models.CASCADE
	)
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATING_CHOICES)
	comment = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Review(id={self.id}, transaction_id={self.transaction_id}, rating={self.rating})"
