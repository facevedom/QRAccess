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


class EventCreation(forms.Form):

    def __init__(self, *args, **kwargs):
        logged_user = kwargs.pop('logged_user', None)
        super(EventCreation, self).__init__(*args, **kwargs)
        if logged_user:
            company = Company.objects.get(name=logged_user)
            self.fields['allowed_rooms'] = forms.ModelMultipleChoiceField(
                                                queryset=Room.objects.filter(company=company).order_by('name'),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False
                                           )

    name = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    description = forms.CharField(widget=forms.Textarea)

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date < start_date:
            msg = u"End date should be after start date."
            self._errors["start_date"] = self.error_class([msg])
