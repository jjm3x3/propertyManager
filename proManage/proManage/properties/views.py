from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Property, Unit, TenantInfo, UnitGroup, User, Group, WorkOrder
from django import forms
from django.contrib.auth.decorators import permission_required

### Forms ### 

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['unit', 'problem', 'cost', 'status']

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'city', 'state', 'zipcode', 'name']

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['size', 'aptType', 'rentalFee', 'unitNumber']

### User CRUD Functions ###

def user_list(request, template_name='properties/user_list.html'):
    users = User.objects.all()
    data = {}
    data['object_list'] = users
    return render(request, template_name, data)
	
def landing(request, template_name='properties/landing.html'):
    data = {}
    return render(request, template_name, data)

def user_create(request, template_name='properties/user_form.html'):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'form':form,'isNew':True})

def user_update(request, pk, template_name='properties/user_form.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        user.set_password(user.password)
        form.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'form':form, 'object':user})

def user_delete(request, pk, template_name='properties/user_confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('properties:user_list')
    return render(request, template_name, {'object':user})
	
def no_delete(request, pk, template_name='properties/user_confirm_delete.html'):
    return redirect('properties:user_list')

def user_view_groups(request, pk, template_name='properties/user_view_groups.html'):
    user = get_object_or_404(User, pk=pk)
    groups = user.groups.all()
    data = {}
    data['groups_list'] = groups
    return render(request, template_name, data)

def user_view_info(request, pk, template_name='properties/user_view_info.html'):
    user = get_object_or_404(User, pk=pk)
    data = {}
    data['user_info'] = user
    return render(request, template_name, data)

### Property CRUD Functions ###

def property_list(request, template_name='properties/property_list.html'):
    properties = Property.objects.all()
    data = {}
    data['prop_list'] = properties
    return render(request, template_name, data)

def property_create(request, template_name='properties/property_form.html'):
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form,'isNew':True})

def property_update(request, pk, template_name='properties/property_form.html'):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form, 'object':property})

def property_delete(request, pk, template_name='properties/property_confirm_delete.html'):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('properties:property_list')
    return render(request, template_name, {'object':property})

def property_view_info(request, pk, template_name='properties/property_view_info.html'):
    property = get_object_or_404(Property, pk=pk)
    data = {}
    data['property_info'] = property
    data['unit_info'] = property.unit_set.all()
    return render(request, template_name, data)

def property_no_delete(request, pk, template_name='properties/property_confirm_delete.html'):
    return redirect('properties:property_list')

### Unit CRUD Functions ###

def unit_create(request, pk, template_name='properties/unit_form.html'):
    property = get_object_or_404(Property, pk=pk)
    form = UnitForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.building = property
        post.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form,'isNew':True,'address':property.address})

def unit_update(request, pk, template_name='properties/unit_form.html'):
    unit = get_object_or_404(Unit, pk=pk)
    form = UnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return redirect('properties:unit_list')
    return render(request, template_name, {'form':form, 'object':unit})

def unit_delete(request, pk, template_name='properties/unit_confirm_delete.html'):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('properties:property_list')
    return render(request, template_name, {'object':unit})

def unit_view_info(request, pk, template_name='properties/unit_view_info.html'):
    unit = get_object_or_404(Unit, pk=pk)
    data = {}
    data['unit_info'] = unit 
    return render(request, template_name, data)

def unit_no_delete(request, pk, template_name='properties/unit_confirm_delete.html'):
    return redirect('properties:unit_list')

### Work Order CRUD Functions ###

def workorder_list(request, template_name='properties/workorder_list.html'):
    workorders = WorkOrder.objects.all()
    data = {}
    data['object_list'] = workorders
    return render(request, template_name, data)
	
def workorder_create(request, template_name='properties/workorder_form.html'):
    form = WorkOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form,'isNew':True})

def workorders_update(request, pk, template_name='properties/workorder_form.html'):
    workorder = get_object_or_404(WorkOrder, pk=pk)
    form = WorkOrderForm(request.POST or None, instance=workorder)
    if form.is_valid():
        form.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form, 'object':workorder})


