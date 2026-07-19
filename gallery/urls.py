from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('home/',views.home, name='home'),
    path('search/', views.search_songs, name='search'),
    path('song/add/', views.add_song, name='add_song'),
    path('song/<int:song_id>/play/', views.play_song, name='play_song'),
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/all/', views.all_playlists, name='all_playlists'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/edit/', views.edit_playlist, name='edit_playlist'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('playlist/<int:playlist_id>/remove-song/<int:song_id>/', views.remove_song_from_playlist, name='remove_song_from_playlist'),
]
