from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  posts = models.ManyToManyField('Post', blank=True)

  def __str__(self):
    return f"{self.username} ({self.first_name} {self.last_name})"

class Followers(models.Model):
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  followers = models.ManyToManyField(User, blank=True, related_name="following")
  # count = models.IntegerField(default=0)

  def __str__(self):
        return f"{self.user}"

class Post(models.Model):
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  text = models.CharField(max_length=280)
  likes = models.IntegerField(default=0)  

  def __str__(self):
        return f"{self.user} {self.date} {self.likes}"

