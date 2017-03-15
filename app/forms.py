"""
Definition of forms.
"""

from django import forms
from functools import partial
from app.models import Room
from app.models import Company

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class User_self_registration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField()
    event_id = forms.CharField()
    rooms = forms.CharField()


class EventCreation(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        super(EventCreation, self).__init__(*args, **kwargs)
        if user:
            company = Company.objects.get(name=user.username)
            self.fields['allowed_rooms'] = forms.ModelMultipleChoiceField(queryset=Room.objects.filter(company=company).order_by('name'))

    
    name = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    
