from django import forms
from .models import Movie, Rating

STANDARD_CHOICES=[
    ( 1, '영상미'),
    ( 2, '배우연기'),
    ( 3, '감독연출'),
    ( 4, '스토리'),
    ( 5, 'OST'),
]
LIKE_CHOICES = [
    (1, '좋아요'),
    (2, '싫어요'),
]

class RatingForm(forms.ModelForm):
    rank = forms.IntegerField(
        label='영화 어때요?',
        widget=forms.RadioSelect(choices=LIKE_CHOICES, attrs={
            'class': 'form-check-inline'}
            )
        )
    content = forms.CharField(
            max_length=100,
            label='',
            widget=forms.TextInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': '한줄평을 남겨주세요:)',
                    }
                )
        )

    standard = forms.IntegerField(
        label='영화의 어떤 부분이 좋으신가요?',
        widget=forms.RadioSelect(choices=STANDARD_CHOICES, attrs={
            'class': 'form-check-inline'}
            )
        )

    class Meta:
        model = Rating
        fields = ['rank', 'content', 'standard']