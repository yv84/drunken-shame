import sys

from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers

from . import views
from .models import app_module, tables


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

setattr(sys.modules[__name__], 'xapp_patterns', home_patterns)

urlpatterns = patterns('',
    url(r'^', include(xapp_patterns, namespace=app_module)),
)
for table in tables:
    table_name = table.__name__.lower()
    setattr(sys.modules[__name__],
        ''.join([table_name,'_patterns']),
        generic_crud_pattern(table_name.capitalize()))

    urlpatterns += (
        url(r''.join([r'^', table_name, r'/']),
            include(getattr(sys.modules[__name__],
                ''.join([table_name,'_patterns'])),
            namespace=table_name)),
    )

# print(tables_patterns)
# import pdb; pdb.set_trace()



# urlpatterns = patterns(tables_patterns) + patterns('',
#     url(r'^rooms/', include(rooms_patterns, namespace='rooms')),
#     url(r'^users/', include(users_patterns, namespace='users')),
  # url(r'^', include(xapp_patterns, namespace=app_module)),
# )
