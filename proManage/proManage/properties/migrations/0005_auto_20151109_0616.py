# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0004_auto_20151026_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssn', models.CharField(max_length=12)),
                ('phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='PropertyGroup',
            new_name='UnitGroup',
        ),
        migrations.RemoveField(
            model_name='tennantinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='TennantInfo',
        ),
    ]
