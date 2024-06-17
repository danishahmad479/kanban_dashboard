from django import forms
from django.forms import TextInput, Select
from .models import *



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['projects']
        widgets = { 
            'projects': TextInput(attrs={'class': 'form-control'}),
            
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['projects','name', 'status','assigned_to','assigned_by']
        widgets = {
           'projects': forms.Select(attrs={'class': 'form-select'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-select'}),
            'assigned_to' : Select(attrs={'class': 'form-select'}),
            'assigned_by' : Select(attrs={'class': 'form-select'}),
        }


