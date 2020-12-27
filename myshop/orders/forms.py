from django import forms
from django.contrib.auth.models import User
from shop.models import Users
from django.contrib.auth.views import PasswordChangeView
from django.core.validators import RegexValidator
from django.core.validators import *
from django import forms

telephone = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={"class":"email_input", 'placeholder': 'email@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"password_input"}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"class":"password_input"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"class":"password_input"}))
    username = forms.EmailField(label='', widget=forms.EmailInput(attrs={"class":"email_input"}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "password_input"}))
    # phone_n = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
    # phone = forms.CharField(validators=[phone_n], widget=forms.TextInput(attrs={"class": "password_input"}))


    class Meta:
        model = User
        fields = ('username','password')


    def clean_password2(self):
        cd = super(UserRegistrationForm, self).clean()
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('Пользователь с таким логином зарегистрирован', code='user')
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают', code='pass')
        return cd['password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('adress', 'phone_number')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



class OrderCreateForm(forms.Form):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
    patronymic = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= False)
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
    phone_number = forms.CharField(max_length=18, validators=[telephone, MaxLengthValidator], widget=forms.TextInput(attrs={"class": "adress_input", 'placeholder': '79000000000'}), required= True)
    city = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
    street = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
    house = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
    flat = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "adress_input"}), required= False)


# class OrderCreateForm(forms.ModelForm):
#     first_name = forms.CharField()
#     patronymic = forms.CharField()
#     last_name = forms.CharField()
#    # phone_number = forms.CharField(max_length=18, validators=[telephone, MaxLengthValidator], widget=forms.TextInput(attrs={"class": "adress_input"}), required= True)
#     city = forms.CharField()
#     street = forms.CharField()
#     house = forms.CharField()
#     flat = forms.CharField()
#
#     class Meta:
#         model = Users
#         fields = ('adress', 'phone_number')