import sys


from django.views import generic
from django.core.urlresolvers import reverse
from rest_framework import viewsets

from . import serializers
from .models import app_module, u_p23, tables
from .models import (
    Rooms,
    Users,
)
from .forms import (
    RoomsForm,
    UsersForm,
)


app_views = sys.modules[__name__]


class ListVerboseName(object):
    def get_context_data(self, **kwargs):
        context = super(ListVerboseName, self).get_context_data(**kwargs)
        context['list_verbose_name'] = self.model._meta.verbose_name
        context['field_names_list'] = self.model._meta.get_all_field_names()
        return context


class HomeView(generic.TemplateView):
    template_name = "home.html"


class RoomsListView(ListVerboseName, generic.ListView):
    model = Rooms


class RoomsDetailView(ListVerboseName, generic.DetailView):
    model = Rooms


class RoomsCreateView(generic.CreateView):
    form_class = RoomsForm
    model = Rooms

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(RoomsCreateView, self).form_valid(form)



class UsersListView(ListVerboseName, generic.ListView):
    model = Users


class UsersDetailView(ListVerboseName, generic.DetailView):
    model = Users
    template_name = "xapp/users_detail.html"


class UsersCreateView(generic.CreateView):
    form_class = UsersForm
    model = Users

    def form_invalid(self, form):
        response = super(UsersCreateView, self).form_invalid(form)
        return response







#-------------REST app-----------
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
    ViewSet = type(view_set_name, (viewsets.ModelViewSet,), attrs)

    setattr(app_views, view_set_name, ViewSet)
