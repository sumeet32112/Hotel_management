from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=("username","email","password1","password2")

    def save(self,commit=True):
        user=super(NewUserForm,self).save(commit=False)
        if commit:
            user.save()
        return user        

class reservation(forms.Form):
    hotel_name=forms.CharField(max_length=200)
    username=forms.CharField(max_length=200)
    checkin=forms.CharField(max_length=200)
    checkout=forms.CharField(max_length=200)
    room_no=forms.CharField()

class search(forms.Form):
    # ROOM_TYPES = [
    #     ('Single-AC', 'Single-AC'),
    #     ('Double-AC', 'Double-AC'),
    #     ('Single-NON-AC', 'Single NON-AC'),
    #     ('Double-NON-AC', 'Double-NON-AC'),
    # ]
    state=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder': 'state'}),required=True)
    checkin=forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}),required=True)
    checkout=forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}),required=True)  
   # room_type=forms.ChoiceField(choices=ROOM_TYPES)

