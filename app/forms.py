"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

class User_self_registration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    id = forms.IntegerField()
    event_id = forms.CharField()