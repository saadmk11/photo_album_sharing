import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from passlib.hash import pbkdf2_sha256

from .forms import AlbumForm, PhotoForm, PasswordForm
from .models import Album, AlbumCredential
from comments.forms import CommentForm


def index(request):
    ''' The Home Page'''
    return render(request, "album/index.html", {})


@login_required
def album_create(request):
    ''' logged in user can publish Albums.
        if not logged in takes user to login page.
    '''
    # creates a formset for photos with extra 4 forms.
    PhotoFormSet = formset_factory(
        PhotoForm, extra=4,
        max_num=10, validate_max=True,
        min_num=1, validate_min=True)
    if request.method == 'POST':
        album_form = AlbumForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)

        if album_form.is_valid() and formset.is_valid():
            album = album_form.save(commit=False)
            album.user = request.user
            album.save()
            # Assigns Every Photo to The Created Album
            for form in formset:
                photo = form.save(commit=False)
                # if the form has photo then only save the form.
                if photo.image:
                    photo.album = album
                    photo.save()
            return redirect('album:album_details', pk=album.pk)

    else:
        album_form = AlbumForm()
        formset = PhotoFormSet()

    context = {
        'title': 'Album Create',
        'album_form': album_form,
        'formset': formset
    }

    return render(request, "album/album_create.html", context)


@login_required
def add_photo(request, pk):
    '''publisher can upload mode photos to an album'''
    album = get_object_or_404(Album, pk=pk)
    # if logged in user is not the album publisher then shows 404 page.
    if not request.user == album.user:
        raise Http404
    # creates a formset for photos with extra 10 forms.
    PhotoFormSet = formset_factory(
        PhotoForm, extra=10,
        max_num=10, validate_max=True,
        min_num=1, validate_min=True)

    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)

        if formset.is_valid():
            # Assigns Every Photo to The Album
            for form in formset:
                photo = form.save(commit=False)
                # if the form has photo then only save the form.
                if photo.image:
                    photo.album = album
                    photo.save()
            return redirect('album:album_details', pk=album.pk)

    else:
        formset = PhotoFormSet()

    context = {
        'title': 'Upload Photos',
        'formset': formset
    }

    return render(request, "album/add_photo.html", context)


@login_required
def album_list(request):
    '''shows the list of albums publish by the logged in user'''
    queryset = Album.objects.filter(user=request.user)

    context = {
        'title': 'Album List',
        'queryset': queryset
    }

    return render(request, "album/album_list.html", context)


@login_required
def album_details(request, pk):
    '''shows the photos, comments, ratings of an album'''
    album = get_object_or_404(Album, pk=pk)
    # if logged in user is not the album publisher then shows 404 page.
    if not request.user == album.user:
        raise Http404
    photos = album.photos.all()
    comments = album.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # assigns the Comment to the requested album.
            comment.album = album
            comment.save()

            return redirect('album:album_details', pk=album.pk)

    else:
        comment_form = CommentForm()

    context = {
        'album': album,
        'photos': photos,
        'comment_form': comment_form,
        'comments': comments
    }

    return render(request, "album/album_details.html", context)


@login_required
def album_share(request, pk):
    '''Generates url & password for specific album'''
    album = get_object_or_404(Album, pk=pk)
    # if logged in user is not the album publisher then shows 404 page.
    if not request.user == album.user:
        raise Http404

    # create Random Password using python
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for x in range(8))
    # encrypt the password
    encypted_password = pbkdf2_sha256.encrypt(password)
    # creates a credential obj for the album.
    album_cred = AlbumCredential.objects.create(
        album=album, password=encypted_password)

    # generates the shareable url.
    share_url = request.build_absolute_uri(
        reverse('album:album_viewer_page', args=(album_cred.identifier,)))

    context = {
        'album': album,
        'password': password,
        'share_url': share_url
    }

    return render(request, "album/album_share.html", context)


def album_viewer_page(request, identifier):
    '''Anyone can View Album with Correct URL & Password'''
    album_cred = get_object_or_404(AlbumCredential, identifier=identifier)
    session_identifier = request.session.get('identifier', False)
    # if there is no session identifier or the identifier doen't match
    # the album_cred identifier show the password input form.
    if (not session_identifier
            or session_identifier != str(album_cred.identifier)):

        password_form = PasswordForm(request.POST or None)

        if password_form.is_valid():
            password = password_form.cleaned_data.get('password')
            # verify password
            verified = album_cred.verify_password(password)

            if verified:
                # if password verified set session variable.
                request.session['identifier'] = str(album_cred.identifier)
                return redirect(
                    'album:album_viewer_page', identifier=album_cred.identifier)
            else:
                messages.error(request, "Password Doesn't Match.")
    else:
        album = album_cred.album
        photos = album.photos.all()
        comments = album.comments.all()

        comment_form = CommentForm(request.POST or None)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # assigns the Comment to the requested album.
            comment.album = album
            comment.save()

            return redirect(
                'album:album_viewer_page', identifier=album_cred.identifier)

        context = {
            'album': album,
            'photos': photos,
            'comment_form': comment_form,
            'comments': comments
        }

        return render(request, "album/share_page.html", context)

    return render(request, "album/viewer_varification.html", {})
