from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Property(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    building = models.ForeignKey(Property)
    size = models.IntegerField(default=0)
    aptType = models.CharField(max_length=20, default="Apartment")
    rentalFee = models.IntegerField(default=0)
    unitNumber = models.CharField(max_length=5, default="1")

    def __str__(self):
        return str(self.building) + ' (Unit ' + str(self.unitNumber) + ')'

class TenantInfo(models.Model):
    user = models.ForeignKey(User)
    ssn = models.CharField(max_length=12)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user

class UnitGroup(models.Model):
    authGroup = models.ForeignKey(Group)
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return str(self.unit) + ' ' + str(self.authGroup)

class WorkOrder(models.Model):
    createdBy = models.ForeignKey(User)
    unit = models.ForeignKey(Unit)
    postedDate = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(True)
    problem = models.CharField(max_length=2000)
    cost = models.FloatField(null=True)
    access = models.BooleanField()
    status = models.NullBooleanField()

    def __str__(self):
        return self.unit + ' (' + self.postedDate + ')'

class PropertyGroup(models.Model):
    userGroup = models.ForeignKey(Group)
    prop = models.ForeignKey(Property)

    def __str__(self):
        return str(self.prop) + ' ' + str(self.userGroup)


