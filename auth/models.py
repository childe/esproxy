from django.db import models

# Create your models here.


class Auth(models.Model):
    ACTION_CHOICES = (
        (1, '_mapping'),
        (2, '_search'),
        (2, '_search'),
    )

    username = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    allowed = models.BooleanField()
    index_regexp = models.CharField(max_length=255)
    action = models.IntegerField(choices=ACTION_CHOICES)
