import sys
from itertools import chain

from django.contrib.auth.models import User, Group
from rest_framework import serializers


from .models import app_module, u_p23, tables


app_serializers = sys.modules[__name__]



for table in tables:
    table_name = table.__name__

    class Meta:
        model = table
        fields = list(chain(
            ('sheets',),table._meta.get_all_field_names()
        ))

    attrs = {
        u_p23(b'Meta'): Meta,
        u_p23(b'__module__'): __name__,
        u_p23(b'get_all_tables'): lambda *args: table.get_all_tables(),
        u_p23(b'sheets'): serializers.SerializerMethodField('get_all_tables'),
    }
    serializer_name = ''.join([table_name, 'Serializer'])
    Serializer = type(serializer_name,
        (serializers.HyperlinkedModelSerializer,), attrs)

    setattr(app_serializers, serializer_name, Serializer)
