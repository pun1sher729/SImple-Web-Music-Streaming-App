from django.db import models
from django import forms
from datetime import datetime

class customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    doj = models.DateTimeField()
    class Meta:
        ordering =('-doj',)

    def __str__(self):
        return self.email

class song(models.Model):
    title = models.CharField(max_length=50)
    artists = models.CharField(max_length=100)
    duration_s = models.IntegerField()
    songid = models.IntegerField(primary_key=True)
    artistid = models.ForeignKey("artist", on_delete=models.CASCADE, default=0)
    doa = models.DateTimeField()
    class Meta:
        ordering =('-doa',)

    def __str__(self):
        return self.title

class playlist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(customer, on_delete=models.CASCADE)
    class Meta:
        ordering =('id',)
    def __str__(self):
        return self.name

class playlist_user(models.Model):
    playlist_id = models.ForeignKey("playlist", on_delete=models.CASCADE)
    playlist_song = models.ForeignKey("song",on_delete=models.CASCADE)
    def __str__(self):
        return self.playlist_id.name + self.playlist_song.title

class artist(models.Model):
    name = models.CharField(max_length=100)
    artistid = models.IntegerField(primary_key=True)
    doj = models.DateTimeField()
    class Meta:
        ordering =('-doj',)

    def __str__(self):
        return self.name

class signupForm(forms.ModelForm):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    passwd = models.CharField(max_length=25)
    class Meta:
        model = customer
        exclude = ('doj',)

class loginForm(forms.Form):
    email = forms.EmailField()
    passwd = forms.CharField(widget=forms.PasswordInput)

class songForm(forms.ModelForm):
    title = models.CharField(max_length=50)
    artists = models.CharField(max_length=100)
    duration_s = models.IntegerField()
    artistid = models.IntegerField()
    class Meta:
        model = song
        exclude = ('doa','songid',)

class artistForm(forms.ModelForm):
    name = models.CharField(max_length=100)
    class Meta:
        model = artist
        exclude = ('doj','artistid',)

class searchForm(forms.Form):
    songName = forms.CharField()

class create_playlistForm(forms.ModelForm):
    name = models.CharField(max_length=50)
    class Meta:
        model = playlist
        exclude = ('id','user', 'doa',)



