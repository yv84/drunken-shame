from django.conf.urls import patterns, include, url
from .views import HomeView

xapp_patterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
)

urlpatterns = patterns('',
    url(r'^', include(xapp_patterns, namespace='xapp')),
)
