from django.db import models

class CropSuggestion(models.Model):
    SEASON_CHOICES = [
        ('Summer', 'Summer'),
        ('Winter', 'Winter'),
        ('Monsoon', 'Monsoon'),
        ('Spring', 'Spring'),
        ('Year-round', 'Year-round'),
    ]
    
    SOIL_CHOICES = [
        ('Clay', 'Clay'),
        ('Sandy', 'Sandy'),
        ('Loamy', 'Loamy'),
        ('Black', 'Black'),
        ('Red', 'Red'),
        ('Alluvial', 'Alluvial'),
        ('Laterite', 'Laterite'),
    ]
    
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    location = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=50, choices=SOIL_CHOICES)
    crop_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    planting_method = models.TextField(blank=True, null=True)
    water_requirements = models.CharField(max_length=50, blank=True, null=True)
    growth_duration = models.CharField(max_length=50, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.crop_name} - {self.season}, {self.soil_type}"
    
    class Meta:
        verbose_name = "Crop Suggestion"
        verbose_name_plural = "Crop Suggestions"