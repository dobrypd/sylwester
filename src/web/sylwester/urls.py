from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from playlist.views import (HomeView, ContactView, PlaylistView, ProposeView,
                            FlavourView, add_new_track, add_track, remove_track,
                            get_my_list, get_list, get_propose_list, thumb_up,
                            thumb_down, add_new_proposition, set_menu,
                            new_account, add_new_comment, get_top_list)
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^playlist$', login_required(PlaylistView.as_view()),
        name='playlist'),
    url(r'^playlist/add_new_track/$', add_new_track, name='add_new_track'),
    url(r'^playlist/add_track/(?P<track_id>\d+)$', add_track,
        name='add_track'),
    url(r'^playlist/remove_track/(?P<track_id>\d+)$', remove_track,
        name='remove_track'),
    url(r'^playlist/get_my_list$', get_my_list, name='get_my_list'),
    url(r'^playlist/get_list/(?P<how_many>\d+)$', get_list, name='get_list'),
    url(r'^playlist/get_top_list$', get_top_list, name='get_top_list'),


    url(r'^propose$', login_required(ProposeView.as_view()), name='propose'),
    url(r'^propose/get_list$', get_propose_list, name='get_propose_list'),
    url(r'^propose/thumb_up/(?P<prop_id>\d+)$', thumb_up,
        name='thumb_up'),
    url(r'^propose/thumb_down/(?P<prop_id>\d+)$', thumb_down,
        name='thumb_down'),
    url(r'^propose/add_new_proposition/$', add_new_proposition,
        name='add_new_proposition'),
    url(r'^propose/add_new_comment/$', add_new_comment,
        name='add_new_comment'),

    url(r'^flavour$', login_required(FlavourView.as_view()), name='flavour'),
    url(r'^flavour/set/(?P<menu_pos>\d+)$', set_menu,
        name='set_menu'),

    url(r'^contact$', ContactView.as_view(), name='contact'),

    # Auth
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/profile/$', HomeView.as_view(), name='profile'),
    url(r'^accounts/newaccount/$', new_account, name='new_account'),
    url(r'^accounts/external/profile/$', HomeView.as_view(), name='externalprofile'),
    #url(r'^accounts/ajaxlogin/$',  'numberlink.main.views.loginajax', name=''),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'', include('social_auth.urls')),
    #external authorisation via facebook, openid etc.
    #url(r'^accounts/external/', include('socialauth.urls')),

    url(r'^photos/', include('picasso.urls')),

    url(r'^admin/', include(admin.site.urls)),
)