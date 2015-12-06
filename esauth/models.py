from django.db import models

# Create your models here.


class ESAuth(models.Model):
    ACTION_CHOICES = (
        (0, 'all'),
        (1, '_mapping'),
        (2, '_alias'),
        (3, '_search'),
        (4, '_msearch'),
        (5, '_delete'),
    )

    index = models.IntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)
    group = models.CharField(max_length=255, null=True, blank=True)
    allowed = models.BooleanField(default=True)
    index_regexp = models.CharField(max_length=255)
    action = models.IntegerField(choices=ACTION_CHOICES, default=0)
