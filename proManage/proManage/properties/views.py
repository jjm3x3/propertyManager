from django.core.urlresolvers import reverse 
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Property, Unit, Report, TenantInfo, UnitGroup, User, Group, WorkOrder, PropertyGroup
from django import forms
from django.contrib.auth.decorators import permission_required
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm 
from twilio.rest import TwilioRestClient
import datetime

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

class TenantInfoForm(ModelForm):
    class Meta:
        model = TenantInfo
        fields = ['ssn','phone']

class WorkOrderForm(ModelForm):
    access = forms.BooleanField(widget=forms.CheckboxInput())
    problem = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':40}))
    class Meta:
        model = WorkOrder
        fields = ['unit', 'problem', 'cost', 'status','access']

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
    
class ReportForm(ModelForm):
    fileBytes = forms.FileField()
    class Meta:
        model = Report
        fields = ['fileBytes', 'fileDescription']




### Authorization Helper Functions ###

def handle_uploaded_file(file_path):
    print "handle_uploaded_file"
    dest = open(file_path.name,"wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()

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
    userForm = UserCreateForm(request.POST or None)
    infoForm = TenantInfoForm(request.POST or None)
    if userForm.is_valid() and infoForm.is_valid():
        user = userForm.save()
        info = infoForm.save(commit=False)
        print 'here is the user:',
        print user
        info.user = user
        info.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'userForm':userForm, 'infoForm': infoForm, 'isNew':True})

def user_update(request, pk, template_name='properties/user_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    user = get_object_or_404(User, pk=pk)
    #info = TenantInfo.objects.get(user=user)
    if not request.user.id == user.id and not request.user.is_superuser:
        return redirect('properties:sorry')
    userForm = UserForm(request.POST or None, instance=user)
    #infoForm = TenantInfoForm(request.POST or None, instance=info)
    infoForm = TenantInfoForm(request.POST or None)
    if userForm.is_valid() and infoForm.is_valid():
        userForm.save()
        #SinfoForm.save()
        user.set_password(userForm.cleaned_data['password'])
        user.save()
        return redirect('properties:user_list')
    return render(request, template_name, {'userForm':userForm, 'infoForm':infoForm, 'object':user})

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

def remove_manager(request, pk, mgr):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    property = get_object_or_404(Property, pk=pk)
    pg = PropertyGroup.objects.get(prop=property)
    pg.users = [x for x in pg.users if x != int(mgr)]
    pg.save()
    return redirect('properties:property_list')
    
def no_delete(request, pk, template_name='properties/user_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    return redirect('properties:user_list')

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
    
def report_list(request, template_name='properties/report_list.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    reports = Report.objects.all()
    data = {}
    data['report_list'] = reports
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
    
def report_create(request, template_name='properties/report_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if request.method != 'POST':
        form = ReportForm()
    else:
        form = ReportForm(request.POST, request.FILES)
    if form.is_valid():
        report = form.save()
        return redirect('properties:report_list')
    return render(request, template_name, {'form':form,'isNew':True})

def property_update(request, pk, template_name='properties/property_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    property = get_object_or_404(Property, pk=pk)
    pg = PropertyGroup.objects.get(prop=property)
    if not (request.user in User.objects.filter(groups__name="Managers") and check_authorization(request.user, pg.users)) and not request.user.is_superuser:
        return redirect('properties:sorry')
    unit_info = property.unit_set.all()
    managers = User.objects.filter(id__in=pg.users, groups__name="Managers")
    form = PropertyForm(request.POST or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form, 'object':property, 'unit_info':unit_info, 'managers':managers})

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
    
def report_delete(request, pk, template_name='properties/report_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('properties:report_list')
    return render(request, template_name, {'object':report})

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

def remove_tenant(request, pk, ten):
    if not request.user.is_authenticated():
        return redirect("/")
    if not request.user.is_superuser:
        return redirect('properties:sorry')
    unit = get_object_or_404(Unit, pk=pk)
    ug = UnitGroup.objects.get(unit=unit)
    ug.users = [x for x in ug.users if x != int(ten)]
    ug.save()
    pg = PropertyGroup.objects.get(prop=unit.building)
    pg.users = [x for x in pg.users if x != int(ten)]
    pg.save()
    return redirect('properties:property_list')

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
        post.save();
        unitGroup = UnitGroup.objects.create(unit_id=post.id)
        unitGroup.save();
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
    ug = UnitGroup.objects.get(unit=unit)
    tenants = User.objects.filter(id__in=ug.users)
    if form.is_valid():
        form.save()
        return redirect('properties:property_list')
    return render(request, template_name, {'form':form, 'object':unit, 'tenants':tenants})
    
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
    if request.user.is_superuser:
        workorders = WorkOrder.objects.all()
    elif request.user in User.objects.filter(groups__name="Tenants"):
        unit_ids = []
        for ug in UnitGroup.objects.all():
            if request.user.id in ug.users:
                unit_ids.append(ug.unit.id)
        workorders = WorkOrder.objects.filter(id__in=unit_ids)
    else:
        unit_ids = []
        for ug in UnitGroup.objects.all():
            if request.user.id in PropertyGroup.objects.get(prop__exact=ug.unit.building).users:
                unit_ids.append(ug.unit.id)
        workorders = WorkOrder.objects.filter(id__in=unit_ids)
    data = {}
    data['object_list'] = workorders
    return render(request, template_name, data)
    
def workorder_create(request, template_name='properties/workorder_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    form = WorkOrderForm(request.POST or None)
    if form.is_valid():
        workorder = form.save(commit=False)
        workorder.createdBy = request.user
        workorder.lastUpdated = datetime.datetime.now()
        workorder.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form,'isNew':True})

def workorder_update(request, pk, template_name='properties/workorder_form.html'):
    if not request.user.is_authenticated():
        return redirect("/")
    workorder = get_object_or_404(WorkOrder, pk=pk)
    form = WorkOrderForm(request.POST or None, instance=workorder)
    if form.is_valid():
        form.save()
        return redirect('properties:workorder_list')
    return render(request, template_name, {'form':form, 'object':workorder})

#code for SMSes

def sms_me(request, template_name='properteis/SMSme'):
    account_sid = "AC0abe79ee5ba00ffa0971fb00995416b1"
    auth_token = "7376933dda1c1d9818d4651b783158fc"
    client = TwilioRestClient(account_sid, auth_token)
     
     message = client.messages.create(to="+12628256216", from_="+14144228769",
                                          body="Hello there!")
