from django.shortcuts import render
from .forms import CropSuggestionForm
from .models import CropSuggestion

def crop_suggestion_view(request):
    form = CropSuggestionForm()
    crops = []
    form_submitted = False
    
    if request.method == 'POST':
        form = CropSuggestionForm(request.POST)
        if form.is_valid():
            season = form.cleaned_data['season']
            location = form.cleaned_data['location']
            soil_type = form.cleaned_data['soil_type']
            form_submitted = True
            
            # Try for exact match
            exact_match = CropSuggestion.objects.filter(
                season=season,
                soil_type=soil_type,
                location__icontains=location
            )
            
            if exact_match.exists():
                crops = exact_match
            else:
                # Try for match with season and soil type
                soil_match = CropSuggestion.objects.filter(
                    season=season,
                    soil_type=soil_type
                )
                
                if soil_match.exists():
                    crops = soil_match
                else:
                    # Just match by season
                    season_match = CropSuggestion.objects.filter(
                        season=season
                    )
                    
                    if season_match.exists():
                        crops = season_match
    
    context = {
        'form': form,
        'crops': crops,
        'form_submitted': form_submitted
    }
    return render(request, 'crop_suggestion.html', context)