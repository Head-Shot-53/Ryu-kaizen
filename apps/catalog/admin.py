from django.contrib import admin

from apps.catalog.models import (
    Category,
    Collection,
    Color,
    Product,
    ProductImage,
    ProductVariant,
    Size,
)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    autocomplete_fields = ("color", "size",)
    fields = (
        "sku",
        "color",
        "size",
        "price",
        "stock_quantity",
        "is_active",
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    autocomplete_fields = ("color",)
    fields = (
        "image",
        "color",
        "alt_text",
        "is_primary",
        "sort_order",
    )


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "base_price",
        "audience",
        "status",
        "is_featured",
        "created_at",
    )
    list_filter = (
        "status",
        "audience",
        "is_featured",
        "category",
        "collections",
    )
    search_fields = (
        "name",
        "slug",
        "description",
        "variants__sku",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    autocomplete_fields = ("category",)
    filter_horizontal = ("collections",)
    inlines = (
        ProductVariantInline,
        ProductImageInline,
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "product",
        "color",
        "size",
        "price",
        "stock_quantity",
        "is_active",
    )
    list_filter = (
        "is_active",
        "color",
        "size",
    )
    search_fields = ("sku", "product__name")
    autocomplete_fields = (
        "product",
        "color",
        "size",
    )
    list_select_related = (
        "product",
        "color",
        "size",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "color",
        "is_primary",
        "sort_order",
        "created_at",
    )
    list_filter = ("is_primary", "color")
    search_fields = ("product__name", "alt_text")
    autocomplete_fields = ("product", "color")
    list_select_related = ("product", "color")