"""
Definition of forms.
"""

from django import forms


class User_self_registration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    id = forms.IntegerField()
    event_id = forms.CharField()


class Login(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
