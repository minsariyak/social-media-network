from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "user_id": self.user.id,
            "content": self.content,
            "dateCreated": self.dateCreated.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # following = models.ManyToManyField(User, blank=True, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followings')

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # follower = models.ManyToManyField(User, blank=True, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')