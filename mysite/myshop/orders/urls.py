from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView,  PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'^password-change/$', PasswordChangeView.as_view(template_name='pass_change.html', success_url= reverse_lazy('orders:password_change_done')), name='password_change'),
    url(r'^password-change-done/$', PasswordChangeDoneView.as_view(template_name='pass_change_done.html'), name='password_change_done'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.order_create, name='order_create'),
]
