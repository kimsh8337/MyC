from django import forms
from .models import Movie, Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['content', 'standard', 'rank']