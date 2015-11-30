from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Property, Unit, TenantInfo, UnitGroup, User, Group, WorkOrder, PropertyGroup
from django import forms
from django.contrib.auth.decorators import permission_required
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm 

### Forms ### 

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups']

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
	user.save()
	user.groups = self.cleaned_data["groups"]
        if commit:
           user.save()
        return user

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

class AddManagerForm(forms.Form):
    users = User.objects.filter(groups__name='Managers')
    manager = forms.ModelChoiceField(users)

class AddTenantForm(forms.Form):
    users = User.objects.filter(groups__name='Tenants')
    tenant = forms.ModelChoiceField(users)




### Authorization Helper Functions ###

def sorry(request, template_name='properties/sorry.html'):
    return render(request, template_name)

def check_authorization(user, user_group):
    return (user.id in user_group)





### User CRUD Functions ###

def user_list(request, template_name='properties/user_list.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if request.user.is_superuser:
        users = User.objects.all()
    elif request.user in User.objects.filter(groups__name='Managers'):
        user_ids = []
        for prop_group in PropertyGroup.objects.all():
            if request.user.id in prop_group.users:
                user_ids.extend(prop_group.users)
        user_ids = list(set(user_ids))
        users = User.objects.filter(id__in=user_ids)
    else:
        users = User.objects.filter(username=request.user.username)
    data = {}
    data['object_list'] = users
    return render(request, template_name, data)
	
def landing(request, template_name='properties/landing.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    data = {}
    return render(request, template_name, data)

def user_create(request, template_name='properties/user_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    form = UserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'form':form,'isNew':True})

def user_update(request, pk, template_name='properties/user_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    user = get_object_or_404(User, pk=pk)
    if not request.user.id == user.id and not request.user.is_superuser:
        return redirect('properties:sorry')
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'form':form, 'object':user})

def user_delete(request, pk, template_name='properties/user_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('properties:user_list')
    return render(request, template_name, {'object':user})
	
def no_delete(request, pk, template_name='properties/user_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    return redirect('properties:user_list')

def user_view_groups(request, pk, template_name='properties/user_view_groups.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    user = get_object_or_404(User, pk=pk)
    groups = user.groups.all()
    data = {}
    data['groups_list'] = groups
    return render(request, template_name, data)

def user_view_info(request, pk, template_name='properties/user_view_info.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    user = get_object_or_404(User, pk=pk)
    data = {}
    data['user_info'] = user
    return render(request, template_name, data)




### Property CRUD Functions ###

def add_manager(request, pk, template_name='properties/add_manager.html'):
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    property = get_object_or_404(Property, pk=pk)
    form = AddManagerForm(request.POST or None)
    if form.is_valid():
        pg = PropertyGroup.objects.get(prop=property)
        mgr = form.cleaned_data['manager']
        mgr_id = User.objects.get(username=mgr).id
        pg.users.append(mgr_id)
        pg.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form})

def property_list(request, template_name='properties/property_list.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if request.user.is_superuser:
        properties = Property.objects.all()
    else:
        prop_ids = []
        for pg in PropertyGroup.objects.all():
            if request.user.id in pg.users:
                prop_ids.append(pg.prop.id)
        properties = Property.objects.filter(id__in=prop_ids)
    data = {}
    data['prop_list'] = properties
    return render(request, template_name, data)

def property_create(request, template_name='properties/property_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        prop = form.save()
        propGroup = PropertyGroup.objects.create(prop_id=prop.id)
        propGroup.save();
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form,'isNew':True})

def property_update(request, pk, template_name='properties/property_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    property = get_object_or_404(Property, pk=pk)
    pg = PropertyGroup.objects.get(prop=property)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
        return redirect('properties:sorry')
    unit_info = property.unit_set.all()
    form = PropertyForm(request.POST or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form, 'object':property, 'unit_info':unit_info})

def property_delete(request, pk, template_name='properties/property_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('properties:property_list')
    return render(request, template_name, {'object':property})

def property_view_info(request, pk, template_name='properties/property_view_info.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    property = get_object_or_404(Property, pk=pk)
    pg = PropertyGroup.objects.get(prop=property)
    if not check_authorization(request.user, pg.users) and not request.user.is_superuser:
        return redirect('properties:sorry')
    data = {}
    data['property_info'] = property
    data['unit_info'] = property.unit_set.all()
    return render(request, template_name, data)

def property_no_delete(request, pk, template_name='properties/property_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    return redirect('properties:property_list')





### Unit CRUD Functions ###

def add_tenant(request, pk, template_name='properties/add_tenant.html'):
    unit = get_object_or_404(Unit, pk=pk)
    pg = PropertyGroup.objects.get(prop=unit.building)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
        return redirect('properties:sorry')
    form = AddTenantForm(request.POST or None)
    if form.is_valid():
        ug = UnitGroup.objects.get(unit=unit)
        tenant = form.cleaned_data['tenant']
        tenant_id = User.objects.get(username=tenant).id
        pg.users.append(tenant_id)
        pg.save()
        ug.users.append(tenant_id)
        ug.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form})

def unit_create(request, pk, template_name='properties/unit_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    property = get_object_or_404(Property, pk=pk)
    pg = PropertyGroup.objects.get(prop=property)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
	return redirect('properties:sorry')
    form = UnitForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.building = property
        post.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form,'isNew':True,'address':property.address})

def unit_update(request, pk, template_name='properties/unit_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    unit = get_object_or_404(Unit, pk=pk)
    pg = PropertyGroup.objects.get(prop=unit.building)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
        return redirect('properties:sorry')
    form = UnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form, 'object':unit})
	
def logout_view(request, template_name='properties/logout.html'):
    auth.logout(request)
    return redirect('properties:login')

def unit_delete(request, pk, template_name='properties/unit_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    unit = get_object_or_404(Unit, pk=pk)
    pg = PropertyGroup.objects.get(prop=unit.building)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
        return redirect('properties:sorry')
    if request.method == 'POST':
        unit.delete()
        return redirect('properties:property_list')
    return render(request, template_name, {'object':unit})

def unit_view_info(request, pk, template_name='properties/unit_view_info.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    unit = get_object_or_404(Unit, pk=pk)
    data = {}
    data['unit_info'] = unit 
    return render(request, template_name, data)

def unit_no_delete(request, pk, template_name='properties/unit_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    return redirect('properties:unit_list')





### Work Order CRUD Functions ###

def workorder_list(request, template_name='properties/workorder_list.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    workorders = WorkOrder.objects.all()
    data = {}
    data['object_list'] = workorders
    return render(request, template_name, data)
	
def workorder_create(request, template_name='properties/workorder_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    form = WorkOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form,'isNew':True})

def workorders_update(request, pk, template_name='properties/workorder_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    workorder = get_object_or_404(WorkOrder, pk=pk)
    form = WorkOrderForm(request.POST or None, instance=workorder)
    if form.is_valid():
        form.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form, 'object':workorder})


