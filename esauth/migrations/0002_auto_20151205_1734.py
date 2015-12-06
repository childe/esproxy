# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esauth',
            name='action',
            field=models.IntegerField(default=0, choices=[(0, b'all'), (1, b'_mapping'), (2, b'_alias'), (3, b'_search'), (4, b'_msearch'), (5, b'_delete')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='esauth',
            name='group',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='esauth',
            name='username',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
