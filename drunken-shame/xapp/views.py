import sys
import json


from django.core.serializers.json import DjangoJSONEncoder
from django import http
from django.views import generic
from django.core.urlresolvers import reverse
from rest_framework import viewsets, mixins

from . import serializers
from .models import app_module, u_p23, tables


app_views = sys.modules[__name__]


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context, cls=DjangoJSONEncoder)


class ListModels(JSONResponseMixin, generic.TemplateView):
    template_name = None

    def get(self, request, *args, **kwargs):
        context = tables[0].get_all_tables(),
        return self.render_to_response(context)


class HomeView(generic.TemplateView):
    template_name = "rest_template.html"


for table in tables:
    table_name = table.__name__

    attrs = {
        u_p23(b'__module__'): __name__,
        u_p23(b'queryset'): \
            table.objects.all(),
        u_p23(b'serializer_class'): \
            getattr(serializers, ''.join([table_name, 'Serializer'])),
    }

    view_set_name = ''.join([table_name, 'ViewSet'])
    ViewSet = type(
        view_set_name,
        (
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            # mixins.DestroyModelMixin,
            viewsets.GenericViewSet,
        ),
        attrs
    )

    setattr(app_views, view_set_name, ViewSet)
