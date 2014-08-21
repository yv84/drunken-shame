from __future__ import absolute_import

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import utc

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, Field

from .models import Room, User

DATE_FORMAT = '%d/%m/%Y'

class RoomForm(forms.ModelForm):
    class Meta:
        fields = ('department', 'spots',)
        model = Room

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'department',
            'spots',
            ButtonHolder(
                Submit('create', 'Create', css_class='btn-primary')
            )
        )


class UserForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'paycheck', 'date_joined')
        model = User

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'paycheck',
            Field('date_joined', input_formats=[DATE_FORMAT]),
            ButtonHolder(
                Submit('create', 'Create', css_class='btn-primary')
            )
        )
