from django.conf.urls import patterns, include, url

xapp_patterns = patterns(
    '',
)

urlpatterns = patterns('',
    url(r'^', include(xapp_patterns, namespace='xapp')),
)
