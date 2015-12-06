# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esauth', '0002_auto_20151205_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='esauth',
            name='index',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
