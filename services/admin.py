# services/admin.py
from django.contrib import admin
from .models import (
    Category, TransportType, TransportBrand, TransportModel,
    Characteristic, CharacteristicValue, Price, Image,
    Product, Equipment, News, HotOffer
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_popular", "slug")
    list_filter = ("is_popular",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TransportBrand)
class TransportBrandAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_popular", "slug")
    list_filter = ("is_popular",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TransportModel)
class TransportModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_popular", "slug")
    list_filter = ("is_popular",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "value", "measurement_unit", "characteristic")
    list_filter = ("measurement_unit",)
    search_fields = ("title",)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "currency", "type")
    list_filter = ("currency", "type")
    search_fields = ("price",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "url",)
    search_fields = ("url",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "price", "created_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "status", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("status", "created_at", "rank_premium", "rank_hot_offer")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "publish_date", "status")
    search_fields = ("title", "author__username")
    list_filter = ("publish_date", "status")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(HotOffer)
class HotOfferAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "status", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("status", "created_at", "rank_hot_offer")
    prepopulated_fields = {"slug": ("title",)}
