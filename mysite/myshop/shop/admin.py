from django.contrib import admin
from .models import Products, Categories, Collection, Orders, Users

# admin.site.register(Products)
# admin.site.register(Categories)
# admin.site.register(Collection)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Categories, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'price', 'size_xs', 'size_s', 'size_m', 'size_l', 'size_xl',
                    'description', 'id_category', 'id_collection', 'number_of_sold', 'image_1', 'image_2', 'image_3']
    list_filter = ['number_of_sold']
    #list_editable = ['price']
    prepopulated_fields = {'slug': ('product_name',)}
admin.site.register(Products, ProductAdmin)



