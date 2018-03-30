from django import forms

from .models import Album, Photo


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['title', 'description']


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['title', 'image']


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
