from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Property(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    name = models.CharField(max_length=30, null=True)

class Unit(models.Model):
    building = models.ForeignKey(Property)
    size = models.IntegerField(default=0)
    aptType = models.CharField(max_length=20)
    rentalFee = models.IntegerField(default=0)

class TennantInfo(models.Model):
    user = models.ForeignKey(User)
    ssn = models.CharField(max_length=12)
    phone = models.CharField(max_length=20)

class UnitGroup(models.Model):
    authGroup = models.ForeignKey(Group)
    unit = models.ForeignKey(Unit)


