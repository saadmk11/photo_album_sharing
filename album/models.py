import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.urls import reverse

from passlib.hash import pbkdf2_sha256


def upload_location(instance, filename):
    username = instance.album.user.username
    album_id = instance.album.id

    return "photos/{}/{}/{}".format(username, album_id, filename)


class Album(models.Model):
    user = models.ForeignKey(
        User,
        related_name='albums',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse("album:album_details", kwargs={"pk": self.pk})

    def get_ratings(self):
        return self.comments.aggregate(Avg('rating'))['rating__avg']


class AlbumCredential(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE
    )
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=256, blank=True, null=True)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)


class Photo(models.Model):
    album = models.ForeignKey(
        Album,
        related_name='photos',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to=upload_location)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']
