from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing_view'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('add_song', views.add_song_view, name='add_song_view'),
    path('add_artist', views.add_artist_view, name='add_artist_view'),
    path('search', views.search_song, name='search_song'),
    path('create_playlist', views.create_playlist, name='create_playlist'),
    path('delete_playlist', views.delete_playlist, name='delete_playlist'),
    path('select_playlist', views.select_playlist, name='select_playlist'),
    path('view_playlist', views.view_playlist, name='view_playlist'),
    path('logout', views.logout, name='logout')
]
