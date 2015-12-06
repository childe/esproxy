# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ESAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('allowed', models.BooleanField()),
                ('index_regexp', models.CharField(max_length=255)),
                ('action', models.IntegerField(choices=[(1, b'_mapping'), (2, b'_search'), (2, b'_search')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
