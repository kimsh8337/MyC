from django import forms
from .models import Post, Comment

SCORE_CHOICES= [
    ( 1, '1'),
    ( 2, '2'),
    ( 3, '3'),
    ( 4, '4'),
    ( 5, '5'),
]

class PostForm(forms.ModelForm):
    score = forms.IntegerField(
    label='Rank this movie :)',
    widget=forms.RadioSelect(choices=SCORE_CHOICES, attrs={
        'class': 'form-check-inline'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'score', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
