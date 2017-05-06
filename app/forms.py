"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from functools import partial
from app.models import Company
from app.models import Room

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class AttendeeRegistration(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField()
    event_id = forms.CharField(widget=forms.HiddenInput)

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
        cleaned_data = super(EventCreation, self).clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date < start_date:
            msg = u"End date should be after start date."
            self._errors["start_date"] = self.error_class([msg])

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'telephone']