from django.conf.urls import patterns, include, url
from .views import HomeView

from .views import (
    HomeView,
    RoomsListView, RoomsDetailView, RoomsCreateView,
    UsersListView, UsersDetailView, UsersCreateView,
)

xapp_patterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)

room_patterns = patterns('',
    url(r"^$", RoomsListView.as_view(), name="list"),
    url(r'^create/$', RoomsCreateView.as_view(), name='create'),
    url(r"^id/(?P<pk>\d+)/$", RoomsDetailView.as_view(), name="detail"),
)

user_patterns = patterns('',
    url(r"^$", UsersListView.as_view(), name="list"),
    url(r'^create/$', UsersCreateView.as_view(), name='create'),
    url(r"^id/(?P<pk>\d+)/$", UsersDetailView.as_view(), name="detail"),
)

urlpatterns = patterns('',
    url(r'^room/', include(room_patterns, namespace='room')),
    url(r'^user/', include(user_patterns, namespace='user')),
    url(r'^', include(xapp_patterns, namespace='xapp')),
)
