"""
Definition of forms.
"""

from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class User_self_registration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField()
    event_id = forms.CharField()
    rooms = forms.CharField()


class EventCreation(forms.Form):
    name = forms.CharField()
    company = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),
               ('d','e'),
               ('d','de'),
               ('d','dr'),
               ('d','dr'),
               ('d','duyi'),
               ('d','yd'),
               ('d','yid'),
               ('d','od'),)
    allowed_rooms = forms.MultipleChoiceField(choices=CHOICES)
