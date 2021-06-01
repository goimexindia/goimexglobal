from django.contrib import admin
from buyerseller.models import Product, Category
from .models import Profile
from mptt.admin import DraggableMPTTAdmin

admin.site.register(Profile)

