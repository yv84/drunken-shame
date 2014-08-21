from django.conf.urls import patterns, include, url
from .views import HomeView

from .views import (
    HomeView,
    RoomListView, RoomDetailView, RoomCreateView,
    UserListView, UserDetailView, UserCreateView,
)

xapp_patterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)

room_patterns = patterns('',
    url(r"^$", RoomListView.as_view(), name="list"),
    url(r'^create/$', RoomCreateView.as_view(), name='create'),
    url(r"^id/(?P<pk>\d+)/$", RoomDetailView.as_view(), name="detail"),
)

user_patterns = patterns('',
    url(r"^$", UserListView.as_view(), name="list"),
    url(r'^create/$', UserCreateView.as_view(), name='create'),
    url(r"^id/(?P<pk>\d+)/$", UserDetailView.as_view(), name="detail"),
)

urlpatterns = patterns('',
    url(r'^room/', include(room_patterns, namespace='room')),
    url(r'^user/', include(user_patterns, namespace='user')),
    url(r'^', include(xapp_patterns, namespace='xapp')),
)
