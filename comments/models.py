from django.db import models

from album.models import Album


class Comment(models.Model):
    album = models.ForeignKey(
        Album,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=64)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True
    )
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-timestamp']
