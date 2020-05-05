from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
	text = models.TextField()
	categories = models.TextField()
	isPinned = models.BooleanField(default=False)
	isFavorited = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="created_by")
	created_at = models.DateTimeField()

#To be implemented later
"""
	class Goal(models.Model):
		text = models.TextField()
		isCompleted = models.BooleanField()
		target_completion_date = models.DateTimeField()
		reminders = models.TextField() ## should be weekly, biweekly, monthly --- could make an enum for this
		categories = models.TextField()
		created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="created_by")
		created_at = models.DateTimeField(auto_now=True)
		completed_at = models.DateTimeField()
"""