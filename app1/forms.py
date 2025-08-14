from django.forms import ModelForm
from django import forms
from .models import CustomUser, Poll, PollOptions


class AddUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',  # Remove default help text
        }


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'start_date', 'end_date']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


PollOptionFormset = forms.inlineformset_factory(Poll, PollOptions, fields=('option_text',), extra=5, can_delete=True)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',  # Remove default help text
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile_number', 'address', 'gender', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',  # Remove default help text
        }
