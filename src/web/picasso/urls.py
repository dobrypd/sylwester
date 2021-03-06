#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include


urlpatterns = patterns('picasso.views',
    url(r'^album/(?P<album>\w+)/$',
        view='view_album',
        name='picasso_view_album'),
    url(r'^albums/$',
        view='list_albums',
        name='picasso_list_albums'),
    url(r'^photo/$',
        view='view_photo',
        name='picasso_view_photo'),
    url(r'^get_photo/(?P<photoid>\w+)/$',
        view='get_photo',
        name='picasso_get_photo'),
    url(r'^get_photo_comments/(?P<photoid>\w+)$',
        view='get_photo_comments',
        name='picasso_view_photo_comments'),
    url(r'^add_new_photo_comment/$',
        view='add_new_photo_comment',
        name='add_new_photo_comment'),
    #url(r'^$',
    #    view='index',
    #    name='picasso_index'),
    url(r'^get_album_comments/(?P<album>\w+)$',
        view='get_album_comments',
        name='picasso_view_album_comments'),

    url(r'^add_new_album_comment/$',
        view='add_new_album_comment',
        name='add_new_album_comment'),
)
