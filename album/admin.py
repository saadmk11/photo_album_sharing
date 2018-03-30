from django.contrib import admin

from .models import Album, Photo, AlbumCredential


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'timestamp',)


class AlbumCredentialAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'identifier',)
    read_only_fields = ('password', 'identifier',)

admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumCredential, AlbumCredentialAdmin)
admin.site.register(Photo)
