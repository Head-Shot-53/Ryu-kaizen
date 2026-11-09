from django.contrib import admin

from apps.catalog.models import Category, Collection, Color, Size


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "is_active",
        "sort_order",
        "created_at",
    )
    list_filter = ("is_active", "parent")
    search_fields = ("name", "description")
    prepopulated_fields = {
        "slug": ("name",),
    }
    ordering = ("sort_order", "name")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "starts_at",
        "ends_at",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {
        "slug": ("name",),
    }
    ordering = ("sort_order", "name")


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code", "created_at")
    search_fields = ("name", "hex_code")
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "sort_order", "created_at")
    search_fields = ("name", "code")
    ordering = ("sort_order", "name")