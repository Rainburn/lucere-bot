from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    site = models.CharField(max_length = 100)
    when = models.CharField(max_length = 150)
    dateissued = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name + '-' + str(self.id)


class User(models.Model):
    userid = models.CharField(max_length = 200, unique=True)
    nickname = models.CharField(max_length = 50)

    def __str__(self):
        return self.nickname


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + ", " + str(self.user)

