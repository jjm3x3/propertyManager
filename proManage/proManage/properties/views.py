from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Property
from .models import Unit
from .models import TenantInfo
from .models import UnitGroup
from .models import User
from .models import Group

# Create your views here.
class PropertyList(ListView):
    model = Property

class PropertyCreate(CreateView):
    model = Property
    success_url = '/'

class PropertyDetail(DetailView):
    model = Property

class PropertyUpdate(UpdateView):
    model = Property

    def get_success_url(self):
        return reverse('properties.detail', kwargs={
            'pk': self.object.pk,
        })

class PropertyDelete(DeleteView):
    model = Property
    success_url = '/'

class UnitList(ListView):
    model = Unit

class TenantInfoList(ListView):
    model = TenantInfo

class UnitGroupList(ListView):
    model = UnitGroup
