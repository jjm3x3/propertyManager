# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_auto_20151129_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertygroup',
            name='managers',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.IntegerField(default=0), size=None),
        ),
        migrations.AddField(
            model_name='unitgroup',
            name='tenants',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.IntegerField(default=0), size=None),
        ),
    ]
