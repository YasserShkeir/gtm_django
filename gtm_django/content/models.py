from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255)

class Content(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    points = models.IntegerField()
    creationDate = models.DateTimeField(auto_now_add=True)
