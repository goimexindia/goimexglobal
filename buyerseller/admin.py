from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin


class ProddisplayAdmin(admin.ModelAdmin):
    list_display = ('productname', 'desc', 'price')


admin.site.register(Proddisplay)

admin.site.register(Rfq)

admin.site.register(RfqImage)

admin.site.register(
    [Admin, ProdComment, Customer, Product, Cart, CartProduct, Order, ProductImage])


class RfqAdmin(admin.ModelAdmin):
    list_display = ['get_status_display']

    class CategoryAdmin(admin.ModelAdmin):
        list_display = ['title', 'parent', 'status']
        list_filter = ['status']

    class CategoryAdmin2(DraggableMPTTAdmin):
        mptt_indent_field = "title"
        list_display = ('tree_actions', 'indented_title',
                        'related_products_count', 'related_products_cumulative_count')
        list_display_links = ('indented_title',)

        def get_queryset(self, request):
            qs = super().get_queryset(request)

            # Add cumulative product count
            qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

            # Add non cumulative product count
            qs = Category.objects.add_related_count(qs,
                                                    Product,
                                                    'category',
                                                    'products_count',
                                                    cumulative=False)
            return qs

        def related_products_count(self, instance):
            return instance.products_count

        related_products_count.short_description = 'Related products (for this specific category)'

        def related_products_cumulative_count(self, instance):
            return instance.products_cumulative_count

        related_products_cumulative_count.short_description = 'Related products (in tree)'

    admin.site.register(Category, CategoryAdmin2)

