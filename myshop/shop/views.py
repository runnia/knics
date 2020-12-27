from django.shortcuts import render, get_object_or_404
from .models import Categories, Products
from cart.forms import CartAddProductForm

import os

def index(request, slug=None):
    products = Products.objects.all()[:4]
    return render(request, 'main.html',
                  {'products': products})

def develop(request):
    return render(request, 'develop.html', {})

def product_list(request, slug=None):
    category = None
    categories = Categories.objects.all()
    products = Products.objects.all()
    if slug == 'develop':
        temp = 'develop.html'
    else:
        temp = 'catalog.html'
        if slug != 'catalog':
            category = Categories.objects.get(slug=slug)
            products = products.filter(id_category=category)

    return render(request,
                  temp,
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug, error=''):
    product = get_object_or_404(Products, id=id)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'itempage.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'error': error})

# ../../develop