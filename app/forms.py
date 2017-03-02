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