import uuid
from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userJoinDate = models.DateField(auto_now_add=True)
    userAge = models.PositiveIntegerField(default=20)

def __str__(self):
    return f"Nome: {self.userName} | Id: {self.userId}"
