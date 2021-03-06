import sys


from rest_framework import serializers

from .models import app_module, u_p23, tables


app_serializers = sys.modules[__name__]

for table in tables:
    table_name = table.__name__

    class Meta:
        model = table
        fields = table._meta.get_all_field_names()
        read_only_fields = ('id',)

    attrs = {
        u_p23(b'Meta'): Meta,
        u_p23(b'__module__'): __name__,
    }
    serializer_name = ''.join([table_name, 'Serializer'])
    Serializer = type(serializer_name,
        (serializers.HyperlinkedModelSerializer,), attrs)

    setattr(app_serializers, serializer_name, Serializer)
