from django.db import models

# Create your models here.


class ESAuth(models.Model):
    # ACTION_CHOICES = (
        # (0, 'all'),
        # (1, '_mapping'),
        # (2, '_alias'),
        # (3, '_search'),
        # (4, '_msearch'),
        # (5, '_delete'),
    # )

    METHOD_CHOICES = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
        (4, 'OPTTION'),
        (5, 'HEAD'),
        (6, '_ALL_'),
    )

    index = models.IntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)
    group = models.CharField(max_length=255, null=True, blank=True)
    allowed = models.BooleanField(default=True)
    # index_regexp = models.CharField(max_length=255)
    request_method = models.IntegerField(choices=METHOD_CHOICES, default=0)
    uri_regexp = models.CharField(max_length=1023, null=False, blank=False, default="")
    response_code = models.IntegerField(default=403, null=True, blank=True)
    response_value = models.CharField(max_length=1023, null=True, blank=True, default="")
