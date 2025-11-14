from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from django.db.models import Avg


class UserSkill(models.Model):
	"""Habilidade associada a um usuário. Modelagem mínima para integração com `services`.

	Nota: é propositalmente simples — pode ser expandida com nível, tags, descrição, etc.
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="skills", on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} — {self.user}"


class UserProfile(models.Model):
	"""Perfil extendido para o usuário.

	Mantemos minimal: relaciona-se 1:1 com o User e contém campos públicos.
	"""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=150, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Profile({self.user.username})"


# Adiciona método `get_average_rating` diretamente ao modelo de usuário ativo.
# Utilizamos `get_user_model()` para suportar tanto o User padrão quanto um custom user.
User = get_user_model()


def get_average_rating(self):
	"""Retorna a média das avaliações (float) recebidas pelo usuário.

	Usa o related_name `reviews_received` definido no modelo `Review` (services).
	Retorna 0.0 se não houver avaliações.
	"""
	avg = self.reviews_received.aggregate(avg=Avg("rating"))["avg"]
	return float(round(avg or 0.0, 2))


# Anexa o método à classe de usuário ativa.
User.add_to_class("get_average_rating", get_average_rating)
