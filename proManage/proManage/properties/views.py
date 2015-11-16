from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Property, Unit, TenantInfo, UnitGroup, User, Group

# Create your views here.

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

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
    return render(request, template_name, {'form':form})

def user_update(request, pk, template_name='properties/user_form.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
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
