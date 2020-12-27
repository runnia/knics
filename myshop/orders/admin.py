from django.contrib import admin
from shop.models import Users


# class OrderItemInline(admin.TabularInline):
#     model = Orders
#     raw_id_fields = ['id_products']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'adress']
    # inlines = [OrderItemInline]

admin.site.register(Users, OrderAdmin)

# Register your models here.
