from django import forms
from django.contrib.auth.models import User

from .models import Song, Playlist


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=150, label="Name")
    email = forms.EmailField(label="Gmail")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class SignInForm(forms.Form):
    email = forms.EmailField(label="Gmail")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'artist', 'link']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Song name'}),
            'artist': forms.TextInput(attrs={'placeholder': 'Artist name'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=200, label="Playlist name")
    song_names = forms.CharField(
        label="Songs",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Enter one song name per line',
        }),
        help_text="Add one song name per line. Songs not yet in the gallery will be skipped."
    )
