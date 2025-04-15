from django.contrib import admin
from .models import CropSuggestion

@admin.register(CropSuggestion)
class CropSuggestionAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'season', 'soil_type', 'location', 'water_requirements')
    list_filter = ('season', 'soil_type')
    search_fields = ('crop_name', 'location', 'description')