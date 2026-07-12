from django.conf import settings
from django.db import models


class Song(models.Model):
    """A single song entry pointing at an external streaming link."""
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    link = models.URLField(max_length=500, help_text="Any streaming link for the song")
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} — {self.artist}"


class Playlist(models.Model):
    """A user-created collection of songs."""
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists'
    )
    songs = models.ManyToManyField(Song, blank=True, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class RecentActivity(models.Model):
    """Tracks songs a user has recently searched for or played."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user} -> {self.song}"
