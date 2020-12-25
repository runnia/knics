import datetime

from django.shortcuts import redirect,render, reverse
from .forms import UserRegistrationForm
from shop.models import Users
from .forms import  LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .backends import EmailBackend
from django.shortcuts import render
from shop.models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('orders:dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                errors = True
                form = LoginForm()
                return render(request, 'login.html', {'form': form,
                                                      'errors': errors})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.email = user_form.cleaned_data['username']
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.save()
            profile = Users.objects.create(user=new_user)
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if user.is_active:
                login(request, user)
                return redirect('orders:dashboard')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    user = Users.objects.get(user_id=request.user.id)
    order = Order.objects.all()
    order = order.filter(email=request.user.email)
    return render(request, 'personal_page.html', {'section': 'dashboard',
                                                  'user': request.user,
                                                  'profile': user,
                                                  'order': order})

@login_required
def order_create(request):
    error =''
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        user = Users.objects.get(user_id=request.user.id)
        if form.is_valid():
            cd = form.cleaned_data
            user.phone_number = cd['phone_number']
            user.patronymic = cd['patronymic']
            request.user.last_name= cd['last_name']
            user.first_name = cd['first_name']
            adress = cd['city'] +' ' + cd['street'] +' ' + cd['house']
            if cd['flat']:
                adrees += ' кв ' + cd['flat']

            Order.objects.create(first_name=cd['first_name'],
                                         last_name = cd['last_name'],
                                         patronymic = cd['patronymic'],
                                         status = 'В обработке',
                                         email = request.user.email,
                                         created = str(datetime.datetime.now()),
                                         phone_number = cd['phone_number'],
                                         adress = adress,)
            user.adress = adress
            user.save()
            request.user.save()
            orders = Order.objects.last()
            for item in cart:
                OrderItem.objects.create(order=orders,
                                         product=item['product'],
                                         size = item['size'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            orders.price = cart.get_total_price()
            orders.save()
            # очистка корзины
            cart.clear()
            return render(request, 'good.html',
                          {'order': orders})
        else:
            error = "Введите телефон в формате 79000000000"

    else:
        form = OrderCreateForm
    return render(request, 'adress.html',
                  {'cart': cart, 'form': form, 'error': error})