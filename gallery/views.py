from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import PlaylistForm, SignInForm, SignUpForm, SongForm
from .models import Playlist, RecentActivity, Song


def test(request):
    return HttpResponse("The app is under construction. Please check back later. Thank you for your patience!  ")

def welcome(request):
    """Landing page with Sign up / Sign in options."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'welcome.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Use the email as the username so sign-in-by-email works cleanly.
            user = User.objects.create_user(
                username=email, email=email, password=password, first_name=name
            )
            user.save()
            messages.success(request, "Account created! You can now sign in.")
            return redirect('welcome')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('gallery:home')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('gallery:home')
            messages.error(request, "That gmail and password don't match any account.")
    else:
        form = SignInForm()
    return render(request,'signin.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('gallery:welcome')


# @login_required   # TEMP: disabled for testing without auth — put this back before shipping
def home(request):
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user)
        recent = RecentActivity.objects.filter(user=request.user).select_related('song')[:6]
    else:
        playlists = Playlist.objects.none()
        recent = []
    return render(request, 'home.html', {
        'playlists': playlists[:4],
        'has_more_playlists': playlists.count() > 4,
        'recent': recent,
    })

# @login_required
def all_playlists(request):
    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'all_playlists.html', {'playlists': playlists})


# @login_required
def search_songs(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = Song.objects.filter(
            Q(name__icontains=query) | Q(artist__icontains=query)
        )
    return render(request, 'search.html', {'query': query, 'results': results})


# @login_required
def play_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    RecentActivity.objects.update_or_create(user=request.user, song=song)
    return render(request,'play_song.html', {'song': song})


# @login_required
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.added_by = request.user
            song.save()
            messages.success(request, f'"{song.name}" was added to the gallery.')
            return redirect('home')
    else:
        form = SongForm()
    return render(request, 'add_song.html', {'form': form})


# @login_required
def create_playlist(request):
    skipped = []
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            raw_names = form.cleaned_data['song_names']
            playlist = Playlist.objects.create(name=name, owner=request.user)

            for line in raw_names.splitlines():
                song_name = line.strip()
                if not song_name:
                    continue
                song = Song.objects.filter(name__iexact=song_name).first()
                if song:
                    playlist.songs.add(song)
                else:
                    skipped.append(song_name)

            if skipped:
                messages.warning(
                    request,
                    "Not loaded (not found in the gallery): " + ", ".join(skipped)
                )
            messages.success(request, f'Playlist "{playlist.name}" created.')
            return redirect('home')
    else:
        form = PlaylistForm()
    return render(request, 'create_playlist.html', {'form': form, 'skipped': skipped})


# @login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    return render(request, 'playlist_detail.html', {'playlist': playlist})


# @login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    skipped = []
    if request.method == 'POST':
        raw_names = request.POST.get('song_names', '')
        for line in raw_names.splitlines():
            song_name = line.strip()
            if not song_name:
                continue
            song = Song.objects.filter(name__iexact=song_name).first()
            if song:
                playlist.songs.add(song)
            else:
                skipped.append(song_name)

        if skipped:
            messages.warning(
                request,
                "Not loaded (not found in the gallery): " + ", ".join(skipped)
            )
        messages.success(request, "Playlist updated.")
        return redirect('playlist_detail', playlist_id=playlist.id)

    return render(request, 'edit_playlist.html', {'playlist': playlist})
