from django.db import migrations

def add_crop_data(apps, schema_editor):
    # Get the CropSuggestion model from the app registry
    CropSuggestion = apps.get_model('myapp', 'CropSuggestion')
    
    # Your crop data to be inserted
    
    crops = [
        # Summer Crops
        {
            'season': 'Summer', 
            'location': 'Punjab', 
            'soil_type': 'Loamy',
            'crop_name': 'Maize',
            'description': 'Maize is a warm-season crop that requires plenty of sunlight and is highly adaptable.',
            'planting_method': 'Direct seeding at 4-5 cm depth with 60-75 cm row spacing.',
            'water_requirements': 'Medium to High',
            'growth_duration': '90-120 days'
        },
        {
            'season': 'Summer', 
            'location': 'Punjab', 
            'soil_type': 'Loamy',
            'crop_name': 'Sugarcane',
            'description': 'Sugarcane is a tropical crop that thrives in warm conditions with adequate moisture.',
            'planting_method': 'Plant cuttings horizontally in furrows.',
            'water_requirements': 'High',
            'growth_duration': '10-12 months'
        },
        {
            'season': 'Summer', 
            'location': 'Gujarat', 
            'soil_type': 'Sandy',
            'crop_name': 'Cotton',
            'description': 'Cotton is a heat-loving crop that requires a long frost-free period.',
            'planting_method': 'Sow seeds 2-4 cm deep in rows 90-120 cm apart.',
            'water_requirements': 'Medium',
            'growth_duration': '150-180 days'
        },
        {
            'season': 'Summer', 
            'location': 'Rajasthan', 
            'soil_type': 'Sandy',
            'crop_name': 'Millet',
            'description': 'Millet is drought-resistant and can grow in poor soil conditions.',
            'planting_method': 'Broadcast or drill seeds at 2-3 cm depth.',
            'water_requirements': 'Low',
            'growth_duration': '60-90 days'
        },
        {
            'season': 'Summer', 
            'location': 'Tamil Nadu', 
            'soil_type': 'Red',
            'crop_name': 'Groundnut',
            'description': 'Groundnut (peanut) is a legume crop that enriches soil with nitrogen.',
            'planting_method': 'Plant seeds 5-7 cm deep in rows 30-45 cm apart.',
            'water_requirements': 'Medium',
            'growth_duration': '90-120 days'
        },
        
        # Winter Crops
        {
            'season': 'Winter', 
            'location': 'Uttar Pradesh', 
            'soil_type': 'Alluvial',
            'crop_name': 'Wheat',
            'description': 'Wheat is a staple food crop that grows well in cool conditions.',
            'planting_method': 'Drill seeds 5 cm deep in rows 20 cm apart.',
            'water_requirements': 'Medium',
            'growth_duration': '120-150 days'
        },
        {
            'season': 'Winter', 
            'location': 'Punjab', 
            'soil_type': 'Loamy',
            'crop_name': 'Barley',
            'description': 'Barley is a hardy cereal grain that can tolerate cold temperatures.',
            'planting_method': 'Drill seeds 2-3 cm deep in rows 15-20 cm apart.',
            'water_requirements': 'Low to Medium',
            'growth_duration': '90-120 days'
        },
        {
            'season': 'Winter', 
            'location': 'Rajasthan', 
            'soil_type': 'Sandy Loam',
            'crop_name': 'Mustard',
            'description': 'Mustard is an oil seed crop that grows well in cooler temperatures.',
            'planting_method': 'Broadcast or drill seeds at 1-2 cm depth.',
            'water_requirements': 'Low',
            'growth_duration': '110-140 days'
        },
        {
            'season': 'Winter', 
            'location': 'Madhya Pradesh', 
            'soil_type': 'Black',
            'crop_name': 'Chickpea',
            'description': 'Chickpea (gram) is a legume that improves soil fertility.',
            'planting_method': 'Drill seeds 5-7 cm deep in rows 30 cm apart.',
            'water_requirements': 'Low',
            'growth_duration': '90-120 days'
        },
        {
            'season': 'Winter', 
            'location': 'Maharashtra', 
            'soil_type': 'Black',
            'crop_name': 'Safflower',
            'description': 'Safflower is an oil seed crop with deep roots that can access moisture in dry soils.',
            'planting_method': 'Drill seeds 3-5 cm deep in rows 45 cm apart.',
            'water_requirements': 'Low',
            'growth_duration': '120-150 days'
        },
        
        # Monsoon Crops
        {
            'season': 'Monsoon', 
            'location': 'West Bengal', 
            'soil_type': 'Alluvial',
            'crop_name': 'Rice',
            'description': 'Rice is a staple food crop that requires standing water during most of its growth.',
            'planting_method': 'Transplant seedlings in puddled soil or direct seeding.',
            'water_requirements': 'Very High',
            'growth_duration': '90-150 days'
        },
        {
            'season': 'Monsoon', 
            'location': 'Maharashtra', 
            'soil_type': 'Black',
            'crop_name': 'Soybean',
            'description': 'Soybean is a legume crop rich in protein and improves soil fertility.',
            'planting_method': 'Drill seeds 3-5 cm deep in rows 30-45 cm apart.',
            'water_requirements': 'Medium',
            'growth_duration': '90-120 days'
        },
        {
            'season': 'Monsoon', 
            'location': 'Karnataka', 
            'soil_type': 'Red',
            'crop_name': 'Ragi',
            'description': 'Ragi (finger millet) is a nutritious cereal crop that is drought-resistant.',
            'planting_method': 'Transplant seedlings or direct seeding.',
            'water_requirements': 'Low to Medium',
            'growth_duration': '90-120 days'
        },
        {
            'season': 'Monsoon', 
            'location': 'Gujarat', 
            'soil_type': 'Sandy Loam',
            'crop_name': 'Pigeon Pea',
            'description': 'Pigeon pea (arhar/tur) is a legume crop that can fix nitrogen in the soil.',
            'planting_method': 'Drill seeds 5 cm deep in rows 60-75 cm apart.',
            'water_requirements': 'Low to Medium',
            'growth_duration': '150-270 days'
        },
        {
            'season': 'Monsoon', 
            'location': 'Andhra Pradesh', 
            'soil_type': 'Red',
            'crop_name': 'Green Gram',
            'description': 'Green gram (moong) is a short-duration pulse crop that improves soil fertility.',
            'planting_method': 'Drill seeds 3-4 cm deep in rows 30 cm apart.',
            'water_requirements': 'Low to Medium',
            'growth_duration': '60-90 days'
        },
        
        # Spring Crops
        {
            'season': 'Spring', 
            'location': 'Uttar Pradesh', 
            'soil_type': 'Alluvial',
            'crop_name': 'Watermelon',
            'description': 'Watermelon is a warm-season fruit crop that requires plenty of space to grow.',
            'planting_method': 'Sow seeds in hills 2-3 cm deep, 1-2 m apart.',
            'water_requirements': 'Medium to High',
            'growth_duration': '80-110 days'
        },
        {
            'season': 'Spring', 
            'location': 'Punjab', 
            'soil_type': 'Loamy',
            'crop_name': 'Cucumber',
            'description': 'Cucumber is a warm-season vegetable crop that grows well in fertile soil.',
            'planting_method': 'Sow seeds 1-2 cm deep in hills or rows.',
            'water_requirements': 'Medium to High',
            'growth_duration': '50-70 days'
        },
        {
            'season': 'Spring', 
            'location': 'Haryana', 
            'soil_type': 'Loamy',
            'crop_name': 'Okra',
            'description': 'Okra (lady finger) is a warm-season vegetable that prefers hot weather.',
            'planting_method': 'Sow seeds 1-2 cm deep in rows 45-60 cm apart.',
            'water_requirements': 'Medium',
            'growth_duration': '50-65 days'
        },
        {
            'season': 'Spring', 
            'location': 'Bihar', 
            'soil_type': 'Alluvial',
            'crop_name': 'Bottle Gourd',
            'description': 'Bottle gourd (lauki) is a vine vegetable that requires support for climbing.',
            'planting_method': 'Sow seeds in hills 2 cm deep, 2-3 m apart.',
            'water_requirements': 'Medium to High',
            'growth_duration': '70-90 days'
        },
        {
            'season': 'Spring', 
            'location': 'Maharashtra', 
            'soil_type': 'Black',
            'crop_name': 'Bitter Gourd',
            'description': 'Bitter gourd (karela) is a tropical vine vegetable with medicinal properties.',
            'planting_method': 'Sow seeds 1-2 cm deep in hills 1-1.5 m apart.',
            'water_requirements': 'Medium',
            'growth_duration': '70-90 days'
        },
        
        # Year-round Crops
        {
            'season': 'Year-round', 
            'location': 'Kerala', 
            'soil_type': 'Laterite',
            'crop_name': 'Coconut',
            'description': 'Coconut is a tropical palm that produces fruits throughout the year.',
            'planting_method': 'Plant seedlings in pits 1m × 1m × 1m, 7-8 m apart.',
            'water_requirements': 'Medium to High',
            'growth_duration': '6-8 years to first fruit, productive for 60+ years'
        },
        {
            'season': 'Year-round', 
            'location': 'Tamil Nadu', 
            'soil_type': 'Red',
            'crop_name': 'Banana',
            'description': 'Banana is a tropical fruit crop that can be grown throughout the year.',
            'planting_method': 'Plant suckers 30 cm deep, 2-3 m apart.',
            'water_requirements': 'High',
            'growth_duration': '10-15 months'
        },
        {
            'season': 'Year-round', 
            'location': 'Karnataka', 
            'soil_type': 'Red',
            'crop_name': 'Papaya',
            'description': 'Papaya is a fast-growing tropical fruit tree with continuous fruiting.',
            'planting_method': 'Sow seeds in nursery and transplant at 2-3 m spacing.',
            'water_requirements': 'Medium',
            'growth_duration': '8-10 months to first fruit, productive for 3-4 years'
        },
        {
            'season': 'Year-round', 
            'location': 'Andhra Pradesh', 
            'soil_type': 'Loamy',
            'crop_name': 'Drumstick',
            'description': 'Drumstick (moringa) is a fast-growing tree with nutritious pods and leaves.',
            'planting_method': 'Plant seedlings or cuttings 3-5 m apart.',
            'water_requirements': 'Low to Medium',
            'growth_duration': '6-8 months to first harvest, productive for many years'
        },
        
    ]

    
    # Insert each crop record into the database
    for crop_data in crops:
        CropSuggestion.objects.create(**crop_data)

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_cropsuggestion'),  # Reference the last migration
    ]

    operations = [
        migrations.RunPython(add_crop_data),  # Run the function to add data
    ]

