from django.conf.urls import url
from .views import (
    index,
    album_create,
    add_photo,
    album_list,
    album_details,
    album_share,
    album_viewer_page,
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^albums/$', album_list, name='album_list'),
    url(r'^albums/create/$', album_create, name='album_create'),
    url(r'^albums/(?P<pk>\d+)/$', album_details, name='album_details'),
    url(r'^albums/(?P<pk>\d+)/add/$', add_photo, name='add_photo'),
    url(r'^albums/(?P<pk>\d+)/share/$', album_share, name='album_share'),
    url(r'^albums/(?P<identifier>[\w-]+)/$',
        album_viewer_page, name='album_viewer_page'),
]
