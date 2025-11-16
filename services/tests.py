from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import UserSkill, UserProfile
from .models import ServiceRequest, Review


class ServicesFeedViewTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user_provider = User.objects.create_user(username="provider", password="x")
		self.user_requester = User.objects.create_user(username="requester", password="x")
		# Profile and location for provider
		UserProfile.objects.create(user=self.user_provider, location="São Paulo")
		skill = UserSkill.objects.create(user=self.user_provider, name="Aulas de Python", description="Ensino do básico ao avançado")
		self.svc = ServiceRequest.objects.create(
			requester=self.user_requester,
			provider=self.user_provider,
			offered_skill=skill,
			description="Preciso de aulas para automação com Python",
		)
		# One review to give provider an average
		Review.objects.create(
			transaction=self.svc,
			reviewer=self.user_requester,
			reviewed_user=self.user_provider,
			rating=5,
			comment="Excelente professor!",
		)

	def test_feed_basic_loads(self):
		url = reverse("services:feed")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, "services/feed.html")
		# Should include the service title
		self.assertContains(resp, "Aulas de Python")

	def test_feed_search_filters(self):
		url = reverse("services:feed")
		# Search by skill name
		resp = self.client.get(url, {"q": "Python"})
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, "Aulas de Python")
		# Search by location
		resp2 = self.client.get(url, {"q": "São Paulo"})
		self.assertEqual(resp2.status_code, 200)
		self.assertContains(resp2, "Aulas de Python")

	def test_root_redirects_to_feed(self):
		resp = self.client.get("/")
		self.assertIn(resp.status_code, (301, 302))
		# Follow redirect and ensure feed renders
		resp_follow = self.client.get("/", follow=True)
		self.assertEqual(resp_follow.status_code, 200)
		self.assertTemplateUsed(resp_follow, "services/feed.html")

# Create your tests here.
