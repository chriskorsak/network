from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  followers = models.ManyToManyField('User', blank=True, related_name="following")

  def __str__(self):
    return f"{self.username} ({self.first_name} {self.last_name})"

class Post(models.Model):
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  text = models.CharField(max_length=280)
  likes = models.ManyToManyField(User, blank=True, related_name="likedbyuser")

  def __str__(self):
        return f"{self.creator} {self.date} {self.likes}"

