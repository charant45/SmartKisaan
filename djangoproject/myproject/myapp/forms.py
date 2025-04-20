# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
import re
from .models import ProductForSale, ProductForRent,CropSuggestion
import pandas as pd
import os


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters long, include a number and a special character."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[^\w\s]', password):
            raise forms.ValidationError("Password must be at least 8 characters long and include at least one number and one special character.")
        return password

class SellForm(forms.ModelForm):
    class Meta:
        model = ProductForSale
        fields = ['image', 'name', 'description', 'category', 'stock', 'price']
        widgets = {
            'category': forms.Select(choices=ProductForSale._meta.get_field('category').choices)
        }


class RentOutForm(forms.ModelForm):
    class Meta:
        model = ProductForRent
        fields = ['image', 'name', 'description', 'category', 'stock', 'rent_price']
        widgets = {
            'category': forms.Select(choices=ProductForRent._meta.get_field('category').choices)
        }




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



# forms.py
import os
import pandas as pd
from django import forms
from .utils import (get_filtered_districts, get_filtered_markets, 
                   get_filtered_commodities, get_filtered_varieties)

# Convert list of values to Django choice tuples
def to_choices(values):
    return [(val, val) for val in values]

def get_dropdown_choices():
    file_path = os.path.join('myapp', 'data', 'market_prices.csv')

    try:
        df = pd.read_csv(file_path, encoding='utf-8')

        # Normalize column names: strip whitespace, remove hidden characters, and convert to lowercase
        df.columns = df.columns.str.strip().str.replace('\u200b', '').str.lower()

        print("Loaded columns:", df.columns.tolist())  # Check column names

        # Ensure 'state' is valid by checking it exists
        if 'state' not in df.columns:
            raise KeyError("'state' column not found in data")

        # Extract the unique values and print them for debugging
        states = sorted(df['state'].dropna().unique())
        districts = sorted(df['district name'].dropna().unique())
        markets = sorted(df['market name'].dropna().unique())
        commodities = sorted(df['commodity'].dropna().unique())
        varieties = sorted(df['variety'].dropna().unique())

        choices = {
            'states': states,
            'districts': districts,
            'markets': markets,
            'commodities': commodities,
            'varieties': varieties
        }

        return choices
    except Exception as e:
        print(f"Error reading dropdowns: {e}")
        return {
            'states': [],
            'districts': [],
            'markets': [],
            'commodities': [],
            'varieties': []
        }


class SellPredictForm(forms.Form):
    state = forms.ChoiceField(label='State')
    district = forms.ChoiceField(label='District')
    market = forms.ChoiceField(label='Market')
    commodity = forms.ChoiceField(label='Commodity')
    variety = forms.ChoiceField(label='Variety')

    def __init__(self, *args, **kwargs):
        super(SellPredictForm, self).__init__(*args, **kwargs)
        
        # Get all choices for initial loading
        choices = get_dropdown_choices()
        
        # Initialize state field with all states
        if choices['states']:
            self.fields['state'].choices = [('', 'Select State')] + to_choices(choices['states'])
        else:
            print("No data for 'state' dropdown.")
            self.fields['state'].choices = [('', 'No states available')]
        
        # Initialize other fields with empty choices
        self.fields['district'].choices = [('', 'Select District')]
        self.fields['market'].choices = [('', 'Select Market')]
        self.fields['commodity'].choices = [('', 'Select Commodity')]
        self.fields['variety'].choices = [('', 'Select Variety')]

        # If form is bound (POST), update choices based on the selected values
        if self.is_bound:
            try:
                # Get selected values (might be invalid at this point)
                selected_state = self.data.get('state', '')
                selected_district = self.data.get('district', '')
                selected_market = self.data.get('market', '')
                selected_commodity = self.data.get('commodity', '')

                # Update district choices based on selected state
                if selected_state:
                    districts = get_filtered_districts(selected_state)
                    self.fields['district'].choices = [('', 'Select District')] + to_choices(districts)
                
                # Update market choices based on selected state and district
                if selected_state and selected_district:
                    markets = get_filtered_markets(selected_state, selected_district)
                    self.fields['market'].choices = [('', 'Select Market')] + to_choices(markets)
                
                # Update commodity choices based on selected state, district, and market
                if selected_state and selected_district and selected_market:
                    commodities = get_filtered_commodities(selected_state, selected_district, selected_market)
                    self.fields['commodity'].choices = [('', 'Select Commodity')] + to_choices(commodities)
                
                # Update variety choices based on selected state, district, market, and commodity
                if selected_state and selected_district and selected_market and selected_commodity:
                    varieties = get_filtered_varieties(selected_state, selected_district, selected_market, selected_commodity)
                    self.fields['variety'].choices = [('', 'Select Variety')] + to_choices(varieties)
                
                print("Updated form choices based on selected values")
            except Exception as e:
                print(f"Error updating form choices: {e}")