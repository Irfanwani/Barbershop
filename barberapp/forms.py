from django import forms
from .models import *


STATUS = (
    ('User', 'User'),
    ('Barber', 'Barber')
)

class addressDetails(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS, label="Login as:")
    class Meta:
        model = userAddress
        fields = ('dp', 'latitude', 'longitude', 'address', 'About', 'website')
        widgets = {
            "About": forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }
        labels = {
            "dp": '',
        }


class fixAppointment(forms.Form):
    datetime = forms.DateTimeField(label="", input_formats=['%m/%d/%Y %I:%M %p'],widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'placeholder': "Date and time for appointment",
            'autocomplete': "off"
        }))
    