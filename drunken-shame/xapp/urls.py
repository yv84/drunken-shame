import sys

from django.conf.urls import patterns, include, url
from rest_framework import routers

from . import views
from .models import app_module, u_p23, tables


urlpatterns = patterns('',)

app_urls = sys.modules[__name__]

#-------------REST app-----------
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# ViewSets define the view behavior.
for table in tables:
    table_name = table.__name__
    view_set_name = ''.join([table_name, 'ViewSet'])
    router.register(table_name.lower(), getattr(views, view_set_name),
        base_name=table_name.lower())

list_models_patterns = patterns('',
    url(r'^963c98e6c3fb42e991e7516ddc8f1096/$', views.ListModels.as_view(), name='list'),
)

urlpatterns += (
    url(r'^api/', include(list_models_patterns, namespace='api-models')),
    url(r'^api/', include(router.urls, namespace='api')),
)

home_patterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
)
setattr(app_urls, 'xapp_patterns', home_patterns)
urlpatterns += (
    url(r'^', include(xapp_patterns, namespace=app_module)),
)
