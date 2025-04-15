from django import forms
from .models import CropSuggestion

class CropSuggestionForm(forms.Form):
    season = forms.ChoiceField(
        choices=CropSuggestion.SEASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'})
    )
    soil_type = forms.ChoiceField(
        choices=CropSuggestion.SOIL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )