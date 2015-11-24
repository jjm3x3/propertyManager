# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_propertygroup_workorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='status',
            field=models.NullBooleanField(),
        ),
    ]
