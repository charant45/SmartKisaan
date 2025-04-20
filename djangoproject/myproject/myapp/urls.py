from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage_view, name='home'),  

    path('sell/', views.sell_product, name='sell'),
    path('rent_out/', views.rent_out_product, name='rent_out'),
    path('buy/', views.buy_view, name='buy'),
    path('rent_in/', views.rent_in, name='rent_in'),
    path('listings/', views.my_listings_view, name='listings'),  # Changed from 'listings' to match the view name
    
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('rent/<int:product_id>/', views.rent_product, name='rent_product'),

    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),  # You need to implement this view
    
    path('my-orders/', views.my_orders_view, name='my_orders'),

    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    path('what-to-plant/', views.crop_suggestion_view, name='crop_suggestion'),

    path('predict/', views.predict_view, name='predict'),
    path('ajax/districts/', views.get_districts, name='ajax_districts'),
    path('ajax/markets/', views.get_markets, name='ajax_markets'),
    path('ajax/commodities/', views.get_commodities, name='ajax_commodities'),
    path('ajax/varieties/', views.get_varieties, name='ajax_varieties'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
