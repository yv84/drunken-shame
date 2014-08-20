from django.conf.urls import patterns, include, url

from .views import SignUpView, LoginView, LogoutView


urlpatterns = patterns('',
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
