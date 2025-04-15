# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
import re

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
