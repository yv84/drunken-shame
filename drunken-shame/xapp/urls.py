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
    router.register(table_name.lower(), getattr(views, view_set_name))

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += (
    url(r'^app/', include(router.urls)),
)

#---------Class based app--------
home_patterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
)

generic_crud_pattern = lambda table: patterns('',
    url(r"^$", getattr(views,
        ''.join([table,'ListView'])).as_view(), name="list"),
    url(r'^create/$', getattr(views,
        ''.join([table,'CreateView'])).as_view(), name='create'),
    url(r"^id/(?P<pk>\d+)/$", getattr(views,
        ''.join([table,'DetailView'])).as_view(), name="detail"),
)

setattr(app_urls, 'xapp_patterns', home_patterns)

for table in tables:
    table_name = table.__name__.lower()
    setattr(app_urls,
        ''.join([table_name,'_patterns']),
        generic_crud_pattern(table_name.capitalize()))

    urlpatterns += (
        url(r''.join([r'^', table_name, r'/']),
            include(getattr(app_urls,
                ''.join([table_name,'_patterns'])),
            namespace=table_name)),
    )

urlpatterns += (
    url(r'^', include(xapp_patterns, namespace=app_module)),
)
