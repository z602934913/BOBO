from django.contrib import admin
from .models import CommoditySKU,CommodityType,Commodity,CommdityImage,IndexCommdityBanner,IndexTypeCommdityBanner,IndexPromotioinBanner
# Register your models here.

admin.site.register(Commodity)
admin.site.register(CommdityImage)
admin.site.register(CommodityType)
admin.site.register(CommoditySKU)
admin.site.register(IndexCommdityBanner)
admin.site.register(IndexTypeCommdityBanner)
admin.site.register(IndexPromotioinBanner)



