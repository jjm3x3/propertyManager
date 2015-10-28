# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_auto_20151022_1908'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TennantInto',
            new_name='TennantInfo',
        ),
    ]
