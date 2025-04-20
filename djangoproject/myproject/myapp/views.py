import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignupForm, SellForm, RentOutForm
from django.contrib.auth.decorators import login_required
from .models import CATEGORY_CHOICES 
from .models import ProductForSale, ProductForRent, CartItem, Order
from django.db import transaction
from decimal import Decimal
from .forms import CropSuggestionForm
from .models import CropSuggestion
from .forms import SellPredictForm
from .ai_model.predictor import get_best_sell_date
import pandas as pd
import os


# Homepage view
def homepage_view(request):
    return render(request, 'home.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def sell_product(request):
    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)  # ✅ Add request.FILES here
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('buy')
    else:
        form = SellForm()
    return render(request, 'sell.html', {'form': form})


@login_required
def rent_out_product(request):
    if request.method == 'POST':
        form = RentOutForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('rent_in')
    else:
        form = RentOutForm()
    return render(request, 'rent_out.html', {'form': form})

# ✅ Updated Buy View with Category Filter
def buy_view(request):
    products = ProductForSale.objects.filter(is_sold_out=False)
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    return render(request, 'buy.html', {
        'products': products,
        'category_choices': CATEGORY_CHOICES
    })


# Default buy view (can be removed if buy_view is used everywhere)
def buy(request):
    products = ProductForSale.objects.all()
    return render(request, 'buy.html', {'products': products})

def rent_in(request):
    category = request.GET.get('category')
    products = ProductForRent.objects.filter(is_rented_out=False)

    if category:
        products = products.filter(category=category)

    return render(request, 'rent_in.html', {
        'products': products,
        'category_choices': CATEGORY_CHOICES
    })


@login_required
def buy_product(request, product_id):
    product = get_object_or_404(ProductForSale, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if product.stock >= quantity:
            product.stock -= quantity
            if product.stock == 0:
                product.is_sold_out = True
            product.save()
            messages.success(request, "Product purchased!")
        else:
            messages.error(request, "Not enough stock!")
    
    return redirect('buy')


@login_required
def rent_product(request, product_id):
    product = get_object_or_404(ProductForRent, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if product.stock >= quantity:
            product.stock -= quantity
            if product.stock == 0:
                product.is_rented_out = True
            product.save()
            messages.success(request, "Product rented!")
        else:
            messages.error(request, "Not enough stock!")

    return redirect('rent_in')



@login_required
def my_listings_view(request):
    sale_products = ProductForSale.objects.filter(seller=request.user)
    rent_products = ProductForRent.objects.filter(owner=request.user)
    
    return render(request, 'my_listings.html', {
        'sale_products': sale_products,
        'rent_products': rent_products
    })


from .forms import SellForm, RentOutForm

@login_required
def edit_product(request, product_id):
    # Check if the product is for sale or rent
    product = ProductForSale.objects.filter(id=product_id, seller=request.user).first()
    form_class = SellForm
    redirect_view = 'my_listings_view'

    if not product:
        product = ProductForRent.objects.filter(id=product_id, owner=request.user).first()
        form_class = RentOutForm

    if not product:
        messages.error(request, "Product not found or unauthorized.")
        return redirect('my_listings_view')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('my_listings_view')
    else:
        form = form_class(instance=product)

    return render(request, 'edit_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = ProductForSale.objects.filter(id=product_id, seller=request.user).first()
    if not product:
        product = ProductForRent.objects.filter(id=product_id, owner=request.user).first()

    if not product:
        messages.error(request, "Product not found or unauthorized.")
    else:
        product.delete()
        messages.success(request, "Product deleted.")

    return redirect('my_listings_view')





def add_to_cart(request, product_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('buy')

    is_rent = request.POST.get('is_rent') == 'true'
    quantity = int(request.POST.get('quantity', 1))
    rental_days = int(request.POST.get('rental_days', 1)) if is_rent else 1

    # Get session key
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Choose correct model
    if is_rent:
        product = get_object_or_404(ProductForRent, id=product_id)
    else:
        product = get_object_or_404(ProductForSale, id=product_id)

    # Check stock
    if quantity > product.stock:
        messages.error(request, "Not enough stock.")
        return redirect('rent_in' if is_rent else 'buy')

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product_id=product.id,
        is_rent=is_rent,
        defaults={'quantity': quantity, 'rental_days': rental_days}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, "Item added to cart.")
    return redirect('view_cart')




def view_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    # Get product instances for each cart item
    items = []
    total = 0
    for item in cart_items:
        product = item.get_product()
        item.product = product  # Attach the product to the item for template usage
        
        if item.is_rent:
            item.subtotal = product.rent_price * item.quantity * item.rental_days
        else:
            item.subtotal = product.price * item.quantity
            
        total += item.subtotal
        items.append(item)
    
    # Count items for cart badge
    cart_count = sum(item.quantity for item in items)
    request.session['cart_count'] = cart_count
    
    return render(request, 'cart.html', {
        'cart_items': items, 
        'total': total,
        'cart_count': cart_count
    })




# views.py

from .models import Order, OrderItem, CartItem, ProductForSale, ProductForRent
from decimal import Decimal


def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        messages.error(request, "Cart is empty.")
        return redirect('view_cart')

    try:
        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            total_order_price = Decimal('0.00')

            for item in cart_items:
                product = item.get_product()

                if item.quantity > product.stock:
                    messages.error(request, f"Not enough stock for {product.name}.")
                    return redirect('view_cart')

                product.stock -= item.quantity
                if product.stock == 0:
                    if item.is_rent:
                        product.is_rented_out = True
                    else:
                        product.is_sold_out = True
                product.save()

                price = product.rent_price if item.is_rent else product.price
                subtotal = price * item.quantity * (item.rental_days if item.is_rent else 1)
                total_order_price += subtotal

                OrderItem.objects.create(
                    order=order,
                    product_name=product.name,
                    is_rent=item.is_rent,
                    quantity=item.quantity,
                    rental_days=item.rental_days,
                    price=price,
                    image_url=product.image.url if product.image else None,
                )

            order.total_price = total_order_price
            order.save()

            cart_items.delete()
            messages.success(request, "Order placed successfully.")
    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('view_cart')

    return render(request, 'checkout.html')


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order_items = order.items.all()

        for item in order_items:
            if item.is_rent:
                product = ProductForRent.objects.filter(name=item.product_name).first()
            else:
                product = ProductForSale.objects.filter(name=item.product_name).first()

            if product:
                product.stock += item.quantity

                if item.is_rent:
                    product.is_rented_out = False
                else:
                    product.is_sold_out = False

                product.save()

        order.delete()
        messages.success(request, "Order deleted and stock restored.")

    return redirect('my_orders')


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







import json
from django.http import JsonResponse
from django.shortcuts import render
from .forms import SellPredictForm
from .utils import (
    get_filtered_districts, get_filtered_markets, 
    get_filtered_commodities, get_filtered_varieties
)
from .ai_model.predictor import get_best_sell_date

def predict_view(request):
    result = None
    graph_data = None
    if request.method == 'POST':
        form = SellPredictForm(request.POST)
        if form.is_valid():
            print("Form is valid, cleaned data:", form.cleaned_data)
            
            cd = form.cleaned_data
            try:
                best_day, predictions = get_best_sell_date(
                    cd['district'], cd['state'], cd['market'], cd['commodity'], cd['variety']
                )
                result = f"Best day to sell is {best_day[0].strftime('%d %b %Y')} at predicted price Rs.{int(best_day[1])}/Quintal"
                print("Result calculated:", result)
                
                # Convert predictions to graph_data for frontend
                graph_data = json.dumps([{
                    'date': d.strftime('%d %b'),  # Shorter date format for display
                    'price': float(p)
                } for d, p in predictions])
                
            except Exception as e:
                print(f"Error in prediction: {e}")
                result = "Error calculating prediction. Please check the server logs."
        else:
            print("Form is invalid, errors:", form.errors)
    else:
        form = SellPredictForm()
    
    return render(request, 'predict.html', {
        'form': form,
        'result': result,
        'graph_data': graph_data
    })


def get_districts(request):
    state = request.GET.get('state', '')
    districts = get_filtered_districts(state)
    return JsonResponse({'districts': districts})

def get_markets(request):
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')
    markets = get_filtered_markets(state, district)
    return JsonResponse({'markets': markets})

def get_commodities(request):
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')
    market = request.GET.get('market', '')
    commodities = get_filtered_commodities(state, district, market)
    return JsonResponse({'commodities': commodities})

def get_varieties(request):
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')
    market = request.GET.get('market', '')
    commodity = request.GET.get('commodity', '')
    varieties = get_filtered_varieties(state, district, market, commodity)
    return JsonResponse({'varieties': varieties})
