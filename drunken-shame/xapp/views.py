from django.views import generic

from .models import (
    Rooms,
    Users,
)
from .forms import (
    RoomsForm,
    UsersForm,
)

class ListVerboseName():
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
    template_name = "xapp/Users_detail.html"


class UsersCreateView(generic.CreateView):
    form_class = UsersForm
    model = Users

    def form_invalid(self, form):
        response = super(UsersCreateView, self).form_invalid(form)
        return response
