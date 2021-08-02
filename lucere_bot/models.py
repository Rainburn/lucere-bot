from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    site = models.CharField(max_length = 100)
    when = models.CharField(max_length = 150)
    dateissued = models.DateTimeField(default=datetime.now, blank=True)


class User(models.Model):
    userid = models.CharField(max_length = 200, unique=True)
    nickname = models.CharField(max_length = 50)


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

