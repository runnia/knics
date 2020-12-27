from django.conf.urls import url, re_path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[-\w]+)/$',
         views.product_list,
        name='category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
    url(r'^catalog/$', views.product_list, name='catalog'),
    url(r'^develop/$', views.develop, name='develop'),
]

# {% static 'image_for_products/{0}/{1}'.format(image.objects.filter(id_product = product.id), 1.jpg) %}
#{% if product.image_1 %}{{ product.image_1.url }}}{% else %}{% static 'img/no_image.png' %}{% endif %}