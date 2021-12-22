from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class Home(models.Model):
    class Meta:
        verbose_name = 'Home'
        verbose_name_plural = 'Homes'

    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    price = models.FloatField()
    meter = models.CharField(max_length=250)
    class_home = models.CharField(max_length=255)
    floor = models.PositiveIntegerField()
    materials = models.CharField(max_length=255)
    height = models.FloatField()
    company = models.CharField(max_length=255)
    width = models.FloatField()
    longitude = models.FloatField()
    stat = [
        ('новое', 'новое'),
        ('хорошее', 'хорошее'),
        ('нужен ремонт', 'нужен ремонт'),
    ]
    status = models.CharField(max_length=12, choices=stat, default='новое')
    bought = [
        ('продоётся', 'продоётся'),
        ('в аренду', 'в аренду'),
    ]
    buy = models.CharField(max_length=9, choices=bought, default='продоётся')
    visit = models.IntegerField(null=True, default=0)
    who = models.CharField(max_length=255, help_text='как обращаться')
    number = models.CharField(max_length=255, help_text='как можно сзязаться')
    end_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def home_count(self):
        self.visit += 1
        self.save()


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    title = models.CharField(max_length=250, blank=True, null=True, default='photo')
    image = models.ImageField(upload_to='img_publication', blank=True, null=True, default='default.png')
    home = models.ForeignKey(Home, on_delete=CASCADE)

    def __str__(self):
        return self.title


class Video(models.Model):
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    title = models.CharField(max_length=250)
    vid = models.FileField()

    def __str__(self):
        return self.title


class Report(models.Model):
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    title = models.CharField(max_length=255)
    text = models.TextField()
    home = models.ForeignKey(Home, on_delete=CASCADE)

    def __str__(self):
        return self.title

    def call_home(self):
        return self.home


class ReportImage(models.Model):
    class Meta:
        verbose_name = 'ReportImage'
        verbose_name_plural = 'ReportImages'

    image = models.ImageField(upload_to='img_publication', blank=True, null=True, default='default.png')
    report = models.ForeignKey(Report, on_delete=CASCADE)


class NewUser(AbstractUser):
    class Meta:
        verbose_name = 'US'
        verbose_name_plural = 'USS'

    stat = [
        ('C', "частное лицо"),
        ('K', "строительная компания")
    ]
    status = models.CharField(max_length=2, choices=stat)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=8)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['status', 'username', 'password']

    def __str__(self):
        return self.username
