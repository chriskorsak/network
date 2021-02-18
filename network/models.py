from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  pass
  followers =
  following = 

# create classes for posts, likes, and followers. not sure if i need following and followers classes independently.

class Post(models.Model):
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  date = DateTimeField(auto_now_add=True)
  text = models.CharField(max_length=280)
  likes = models.IntegerField(default=0)

  def __str__(self):
        return f"{self.user} {self.date} {self.likes}"

