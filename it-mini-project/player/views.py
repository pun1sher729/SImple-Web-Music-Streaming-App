from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse
from .models import *

def landing_view(request):
    if request.method == 'GET':
        try:
            cur_email = request.session.get("email")
            if cur_email != None:
                login=1
            else:
                login=0
        except:
            request.session["email"] = None
            login=0
        if login==0:
            return render(request,'index.html', {'login':login, 'cur_email':cur_email})
        else:
            return render(request,'main.html', {'login':login, 'cur_email':cur_email})
    elif request.method=='POST' and request.session["email"]:
        if 'search' in request.POST:
            return redirect("search_song")
        elif 'view' in request.POST:
            return redirect('view_playlist')
        elif 'create' in request.POST:
            return redirect('create_playlist')


def login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get("email")
            passwd = cd.get("passwd")
            check_if_user_exists = customer.objects.filter(email=email).exists()
            if check_if_user_exists:
                user = customer.objects.get(email=email)
                if passwd == user.passwd:
                    request.session["email"] = email
                    return redirect('landing_view')
                else:
                    return render(request, 'login.html', {"op": "Wrong password"})
            else:
                return render(request, 'login.html', {"op": "Email not found"})
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'login.html', {"op": error_string})
    elif request.method == 'GET':
        return render(request,'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.doj = datetime.now()
            post.save()
            return redirect('login_view')
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'signup.html', {"op": error_string})
    elif request.method=='GET':
        return render(request,'signup.html')

def add_song_view(request):
    if request.method == 'GET':
        return render(request, 'add_song.html')
    elif request.method == 'POST':
        form = songForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.doa = datetime.now()
            post.songid = 2000 + len(song.objects.all()) + 1
            post.save()
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'add_song.html', {"op": error_string})
        return redirect("add_song_view")

def add_artist_view(request):
    if request.method == 'GET':
        return render(request, 'add_artist.html')
    elif request.method == 'POST':
        form = artistForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.doj = datetime.now()
            post.artistid = 1000 + len(artist.objects.all()) + 1
            post.save()
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'add_artist.html', {"op": error_string})
        return redirect("add_artist_view")

def search_song(request):
    if request.method == 'GET' and request.session["email"]: 
        return render(request, 'search.html' ,{'cur_email':request.session["email"]})
    elif request.session["email"] == None:
        return redirect("landing_view")
    elif request.method == 'POST' and request.POST['search']:
        form = searchForm(request.POST)
        if form.is_valid() and request.session["email"]:
            songName = form.cleaned_data.get('songName')
            all_songs = song.objects.all()
            headers = ['Title', 'Artist']
            search_output = {}
            artists = {}
            for s in all_songs:
                if songName.lower() in s.title.lower():
                    search_output[s.songid] = []
                    search_output[s.songid].append(s.title)
                    search_output[s.songid].append(s.artists)
            return render(request, 'search.html', {'cur_email':request.session["email"],"headers":headers ,"search_output": search_output})
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            return render(request, 'search.html', {'cur_email':request.session["email"],"op": error_string})
    return redirect("search_song")

def create_playlist(request):
    if request.method == 'GET' and request.session["email"]:
        cur_user = customer.objects.get(email=request.session["email"])
        if len(playlist.objects.filter(user=cur_user)) != 0:
            cur_playlists_header = "Playlists"
            cur_playlists = {}
            for p in playlist.objects.filter(user=cur_user):
                cur_playlists[p.id] = p.name.upper()
            return render(request, 'create_playlist.html', {'cur_email':request.session["email"],'cur_playlists_header':cur_playlists_header, 'cur_playlists':cur_playlists})
        return render(request, 'create_playlist.html')
    elif request.session["email"] == None:
        return redirect("landing_view")
    elif request.method == 'POST' and request.session["email"]:
        form = create_playlistForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id = 3001 + len(playlist.objects.all())
            post.user = customer.objects.get(email=request.session["email"])
            post.doa = datetime.now()
            post.save()
        cur_user = customer.objects.get(email=request.session["email"])
        if len(playlist.objects.filter(user=cur_user)) != 0:
            cur_playlists_header = "Playlists"
            cur_playlists = {}
            for p in playlist.objects.filter(user=cur_user):
                cur_playlists[p.id] = p.name.upper()
            return render(request, 'create_playlist.html', {'cur_email':request.session["email"],'cur_playlists_header':cur_playlists_header, 'cur_playlists':cur_playlists})
    return render(request, 'create_playlist.html')

def delete_playlist(request):
    if request.method == 'POST':
        playlist_id = request.POST['delete']
        playlist.objects.get(id=playlist_id).delete()
    return redirect("create_playlist")

def select_playlist(request):
    if request.method == 'POST' and request.session["email"] and ('add' in request.POST):
        print(request.POST)
        song_id = request.POST['add']
        song_name = song.objects.get(songid=song_id)
        cur_email = request.session["email"]
        cur_user = customer.objects.get(email=cur_email)
        user_playlists = playlist.objects.filter(user=cur_user)
        playlists = {}
        for p in user_playlists:
            playlists[p.id] = p.name
        if len(playlists)>0:
            show_playlists=1
        else:
            show_playlists=0
        return render(request, "search.html", {"song_name":song_name,"show_playlists":show_playlists, "playlists":playlists, "song_id":song_id})
    elif request.method == 'POST' and request.session["email"] and 'add_to_playlist' in request.POST:
        print(request.POST)
        song_id = request.POST['add_to_playlist']
        playlist_id = request.POST['playlist']
        cur_song = song.objects.get(songid=song_id)
        cur_playlist = playlist.objects.get(id=playlist_id)
        song_to_playlist = playlist_user.objects.create(playlist_id=cur_playlist, playlist_song=cur_song)
        song_to_playlist.save()
    return redirect("search_song")

def view_playlist(request):
    if request.method == "GET" and request.session['email']:
        cur_email = request.session['email']
        cur_user = customer.objects.get(email=request.session['email'])
        playlists = playlist.objects.filter(user=cur_user)
        user_playlists = {}
        for p in playlists:
            user_playlists[p.id] = p.name.upper()
        show_songs=0
        return render(request, "view_playlists.html", {'show_songs':show_songs,"user_playlists":user_playlists})
    elif request.method=='POST' and request.session['email'] and 'playlist' in request.POST:
        playlist_id = request.POST['playlist']
        cur_playlist = playlist.objects.get(id=playlist_id)
        playlist_name = cur_playlist.name
        playlist_songs = playlist_user.objects.filter(playlist_id=cur_playlist)
        songs = {}
        headers = ['Title', 'Artist']
        for s in playlist_songs:
            songs[s.playlist_song.songid]=[]
            songs[s.playlist_song.songid].append(s.playlist_song.title)
            songs[s.playlist_song.songid].append(s.playlist_song.artists)
        if len(songs)>0:
            show_songs=1
            len_songs=1
        else:
            show_songs=1
            len_songs=0
        return render(request, "view_playlists.html", {'show_songs':show_songs ,'playlist_name':playlist_name, 'headers':headers,'songs':songs, 'len':len_songs})

def logout(request):
    request.session['email'] = None
    return redirect("landing_view")