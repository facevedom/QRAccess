"""
Definition of forms.
"""

from django import forms


class User_self_registration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField()
    event_id = forms.CharField()
    rooms = forms.CharField()


class Login(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
