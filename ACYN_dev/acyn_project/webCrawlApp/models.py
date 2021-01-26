from django.db import models

# Create your models here.
class NaverWebtoon(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    thumbnail = models.CharField(max_length=500)


class NaverWebnovel(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    thumbnail = models.CharField(max_length=500)

class DaumWebtoon(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    thumbnail = models.CharField(max_length=500)

class Netflix(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    thumbnail = models.CharField(max_length=500)