"""ph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve

from views import index, search_results, search_from_tags
import notifications.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^posts/', include('posts.urls')),

    url(r'^search/', search_results, name='search_results'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^results/', search_results, name='search-results'),
    url(r'^results-tags/(?P<tags>\w+)', search_from_tags, name='search-from-tags'),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
        urlpatterns += [
            url(r'^storage/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT
                }),
        ]