from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=140)
    content = models.TextField()
    author = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    password = models.CharField(max_length=20)
