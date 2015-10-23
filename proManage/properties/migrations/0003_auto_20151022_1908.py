# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('properties', '0002_auto_20151022_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authGroup', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='TennantInto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField(default=0)),
                ('aptType', models.CharField(max_length=20)),
                ('rentalFee', models.IntegerField(default=0)),
                ('building', models.ForeignKey(to='properties.Property')),
            ],
        ),
        migrations.AddField(
            model_name='propertygroup',
            name='unit',
            field=models.ForeignKey(to='properties.Unit'),
        ),
    ]
