from __future__ import absolute_import

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import utc

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, Field

from .models import Rooms, Users


class RoomsForm(forms.ModelForm):
    class Meta:
        fields = ('department', 'spots',)
        model = Rooms

    def __init__(self, *args, **kwargs):
        super(RoomsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'department',
            'spots',
            ButtonHolder(
                Submit('create', 'Create', css_class='btn-primary')
            )
        )

from django.conf import settings

class UsersForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'paycheck', 'date_joined')
        model = Users

    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['date_joined'].widget.format = '%d/%m/%Y'
        self.helper.layout = Layout(
            'name',
            'paycheck',
            Field('date_joined', placeholder='yyyy-mm-dd' ),
            ButtonHolder(
                Submit('create', 'Create', css_class='btn-primary')
            ),
        )
