from django.db import models

# Create your models here.
class TestData(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=30)
    url = models.URLField()
    thumbnail = models.CharField(max_length=500)

class NaverWebtoon(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=30)
    url = models.URLField()
    thumbnail = models.CharField(max_length=500)


class NaverWebnovel(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=30)
    url = models.URLField()
    thumbnail = models.CharField(max_length=500)

class DaumWebtoon(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=30)
    url = models.URLField()
    thumbnail = models.CharField(max_length=500)

class Netflix(models.Model):
    title = models.CharField(max_length=100, null=False)
    intro = models.CharField(max_length=500)
    genre = models.CharField(max_length=30)
    url = models.URLField()
    thumbnail = models.CharField(max_length=500)