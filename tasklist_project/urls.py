# tasklist_project/urls.py

from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasklist.urls')),
    # re_path(r'^some-path/$', some_view, name='some-view'), 
    # path('accounts/', include('allauth.urls')),
]
