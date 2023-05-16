from django.contrib import admin
from .models import *

admin.site.register(customer)
admin.site.register(song)
admin.site.register(artist)
admin.site.register(playlist)
admin.site.register(playlist_user)

# Register your models here.
