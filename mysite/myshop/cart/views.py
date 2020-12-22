import switch as switch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Products
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('cart:cart_detail')
#
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')
#
# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'bucket.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    Size = request.POST.get('Size')
    product = get_object_or_404(Products, id=product_id)
    if product:
        choices = {'XS': product.size_xs,
                   'S': product.size_s,
                   'M': product.size_m,
                   'L': product.size_l,
                   'XL': product.size_xl}
        result = choices.get(Size, 'default')
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if not product:
            result = cd['quantity']
        if result < cd['quantity']:
            error = 'На складе только {0} товаров размера {1}'.format(result, Size)
            cart_product_form = CartAddProductForm()
            return render(request,
                          'itempage.html',
                          {'product': product,
                           'cart_product_form': cart_product_form,
                           'error': error})
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'],
                 size=Size
                 )
    return redirect('cart:cart_detail')

def cart_remove(request, product_id, product = None, Size='M'):
    if request.method == 'POST':
        Size = request.POST.get("Size")
    print(Size)
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product, Size)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'bucket.html', {'cart': cart, 'error': None})


