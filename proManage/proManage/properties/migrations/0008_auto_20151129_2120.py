# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_workorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='unitNumber',
            field=models.CharField(max_length=5, default='1'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='aptType',
            field=models.CharField(max_length=20, default='Apartment'),
        ),
    ]
