import os

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Book list:
    (r'^library/$', 'library.views.library_main'),
    (r'^library/topic/(\w+)/$', 'library.views.library_topic'),
    (r'^library/list/(\w+)/(\d+)/$', 'library.views.library_book_list'),
    (r'^library/detail/(\d+)/$', 'library.views.library_book_detail'),
    #admin
    # Uncomment the next line to enable the admin:
    (r'^schoolsite/admin/', include(admin.site.urls)),
)
#debug static files
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'), )


