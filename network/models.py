from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f'Post: {self.id} Writer by {self.user} on {self.timestamp.strftime('%d-%b-%Y %H:%M:%S')}'


class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_following")
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_follower")

    def __str__(self):
        return f'{self.user} following {self.follower_user}'


class Likes(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_liked")
    post_like = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_who_liked")

    def __str__(self):
        return f'{self.user_like} liked {self.post_like}'

