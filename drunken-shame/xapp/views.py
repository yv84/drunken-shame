from django.views import generic

from .models import (
    Room,
    User,
)
from .forms import (
    RoomForm,
    UserForm,
)

class ListVerboseName():
    def get_context_data(self, **kwargs):
        context = super(ListVerboseName, self).get_context_data(**kwargs)
        context['list_verbose_name'] = self.model._meta.verbose_name
        context['field_names_list'] = self.model._meta.get_all_field_names()
        return context


class HomeView(generic.TemplateView):
    template_name = "home.html"


class RoomListView(ListVerboseName, generic.ListView):
    model = Room


class RoomDetailView(ListVerboseName, generic.DetailView):
    model = Room


class RoomCreateView(generic.CreateView):
    form_class = RoomForm
    model = Room

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(RoomCreateView, self).form_valid(form)



class UserListView(ListVerboseName, generic.ListView):
    model = User


class UserDetailView(ListVerboseName, generic.DetailView):
    model = User
    template_name = "xapp/user_detail.html"


class UserCreateView(generic.CreateView):
    form_class = UserForm
    model = User
