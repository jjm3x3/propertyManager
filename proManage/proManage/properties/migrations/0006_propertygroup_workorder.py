# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('properties', '0005_auto_20151109_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prop', models.ForeignKey(to='properties.Property')),
                ('userGroup', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postedDate', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(verbose_name=True)),
                ('problem', models.CharField(max_length=2000)),
                ('cost', models.FloatField(null=True)),
                ('access', models.BooleanField()),
                ('createdBy', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(to='properties.Unit')),
            ],
        ),
    ]
