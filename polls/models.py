from django.db import models

class Post(models.Model):
    post_text = models.CharField(max_length=200)


class Comment(models.Model):
    question = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)

