from django.urls import path
from . import views

urlpatterns = [
    path('what-to-plant/', views.crop_suggestion_view, name='crop_suggestion'),
]