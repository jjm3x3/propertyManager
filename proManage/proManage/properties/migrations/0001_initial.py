# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
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
                ('name', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('users', django.contrib.postgres.fields.ArrayField(default=list, size=None, base_field=models.IntegerField(default=0), blank=True)),
                ('prop', models.ForeignKey(to='properties.Property')),
            ],
        ),
        migrations.CreateModel(
            name='TenantInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssn', models.CharField(max_length=12)),
                ('phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField(default=0)),
                ('aptType', models.CharField(default=b'Apartment', max_length=20)),
                ('rentalFee', models.IntegerField(default=0)),
                ('unitNumber', models.CharField(default=b'1', max_length=5)),
                ('building', models.ForeignKey(to='properties.Property')),
            ],
        ),
        migrations.CreateModel(
            name='UnitGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authGroup', models.ForeignKey(to='auth.Group')),
                ('unit', models.ForeignKey(to='properties.Unit')),
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
                ('status', models.NullBooleanField()),
                ('createdBy', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(to='properties.Unit')),
            ],
        ),
    ]
