from django.db import models
from django.contrib.auth.models import User

from simple_history.models import HistoricalRecords


class Room(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, default='', unique=True)
    available = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
