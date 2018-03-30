from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = forms.ChoiceField(
        required=False,
        choices=RATING_CHOICES
    )

    class Meta:
        model = Comment
        fields = ['name', 'rating', 'text']
