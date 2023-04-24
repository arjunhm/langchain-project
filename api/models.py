from django.db import models

# Create your models here.

class Post(models.Model):

    topic = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}__{self.topic}"
