from django.views import generic

from .models import (
    Room,
    User,
)


class ListVerboseName():
    def get_context_data(self, **kwargs):
        context = super(ListVerboseName, self).get_context_data(**kwargs)
        context['list_verbose_name'] = self.model._meta.verbose_name
        return context


class HomeView(generic.TemplateView):
    template_name = "home.html"


class RoomListView(ListVerboseName, generic.ListView):
    model = Room


class RoomDetailView(ListVerboseName, generic.DetailView):
    model = Room


class UserListView(ListVerboseName, generic.ListView):
    model = User


class UserDetailView(ListVerboseName, generic.DetailView):
    model = User
    template_name = "xapp/user_detail.html"
