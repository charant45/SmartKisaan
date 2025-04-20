from django.db import models
from django.contrib.auth.models import User

# Define category choices globally
CATEGORY_CHOICES = [
    ('tractor', 'Tractor'),
    ('seeds', 'Seeds'),
    ('tools', 'Tools'),
    ('rotavator', 'Rotavator'),
    ('threshing machine', 'Threshing Machine'),
    ('sprinkler system', 'Sprinkler System'),
    # Add more as needed
]

class ProductForSale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold_out = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ProductForRent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_rented_out = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    session_key = models.CharField(max_length=40)
    product_id = models.PositiveIntegerField()
    is_rent = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    rental_days = models.PositiveIntegerField(default=1)  # Add this field for rental duration

    def get_product(self):
        from .models import ProductForSale, ProductForRent
        return ProductForRent.objects.get(id=self.product_id) if self.is_rent else ProductForSale.objects.get(id=self.product_id)

    def total_price(self):
        product = self.get_product()
        if self.is_rent:
            return product.rent_price * self.quantity * self.rental_days
        else:
            return product.price * self.quantity
        

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    is_rent = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    rental_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)  # If you have image paths

    def subtotal(self):
        if self.is_rent:
            return self.price * self.quantity * self.rental_days
        return self.price * self.quantity
    



    
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