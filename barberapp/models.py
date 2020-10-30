from django.db import models


class userAddress(models.Model):
    dp = models.ImageField(upload_to='images/')
    username = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=1000)
    About = models.TextField(max_length=1000)
    website = models.URLField(blank=True)


class barberAddress(models.Model):
    dp = models.ImageField(upload_to="images/")
    username = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=1000)
    employee_no = models.PositiveIntegerField()
    About = models.TextField(max_length=1000)
    website = models.URLField(blank=True)



class appointmentDetails(models.Model):
    barbername = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    datetime = models.DateTimeField()