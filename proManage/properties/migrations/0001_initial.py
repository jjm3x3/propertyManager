# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
