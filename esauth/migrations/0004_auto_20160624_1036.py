# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esauth', '0003_esauth_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='esauth',
            name='action',
        ),
        migrations.RemoveField(
            model_name='esauth',
            name='index_regexp',
        ),
        migrations.AddField(
            model_name='esauth',
            name='request_method',
            field=models.IntegerField(default=0, choices=[(0, b'GET'), (1, b'POST'), (2, b'PUT'), (3, b'DELETE'), (4, b'OPTTION'), (5, b'HEAD'), (6, b'_ALL_')]),
        ),
        migrations.AddField(
            model_name='esauth',
            name='response_code',
            field=models.IntegerField(default=403, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='esauth',
            name='response_value',
            field=models.CharField(default=b'', max_length=1023, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='esauth',
            name='uri_regexp',
            field=models.CharField(default=b'', max_length=1023),
        ),
        migrations.AlterField(
            model_name='esauth',
            name='allowed',
            field=models.BooleanField(default=True),
        ),
    ]
