from django.contrib import admin
from buyerseller.models import Product, Category
from .models import Profile, Contactme
from mptt.admin import DraggableMPTTAdmin

admin.site.register(Profile)


class ContactmeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')


admin.site.register(Contactme, ContactmeAdmin)
