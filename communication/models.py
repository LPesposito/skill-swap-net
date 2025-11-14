from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
	"""Sala de chat que pode ter múltiplos participantes (Users)."""
	name = models.CharField(max_length=200, blank=True)
	participants = models.ManyToManyField(
		settings.AUTH_USER_MODEL, related_name="chat_rooms", blank=True
	)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.name:
			return f"ChatRoom({self.name})"
		return f"ChatRoom(id={self.id})"


class ChatMessage(models.Model):
	"""Mensagem enviada dentro de uma ChatRoom por um usuário."""
	room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# Truncate content for readability
		summary = (self.content[:47] + "...") if len(self.content) > 50 else self.content
		return f"Message(id={self.id}, sender={self.sender}, room_id={self.room_id}, content={summary})"
