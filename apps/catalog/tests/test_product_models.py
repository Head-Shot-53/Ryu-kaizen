from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.catalog.models import Product, ProductImage, ProductVariant


@pytest.mark.django_db
def test_product_is_created_as_draft(product):
    assert product.status == Product.Status.DRAFT
    assert product.audience == Product.Audience.UNISEX
    assert product.is_featured is False


@pytest.mark.django_db
def test_variant_uses_product_base_price(product, color, size):
    variant = ProductVariant.objects.create(
        product=product,
        color=color,
        size=size,
        sku="RYU-SHOES-BLACK-M",
        stock_quantity=10,
    )

    assert variant.effective_price == Decimal("299.99")


@pytest.mark.django_db
def test_variant_can_override_product_price(product, color, size):
    variant = ProductVariant.objects.create(
        product=product,
        color=color,
        size=size,
        sku="RYU-SHOES-BLACK-M",
        price=Decimal("329.99"),
        stock_quantity=10,
    )

    assert variant.effective_price == Decimal("329.99")


@pytest.mark.django_db
def test_product_variant_combination_must_be_unique(product, color, size):
    ProductVariant.objects.create(
        product=product,
        color=color,
        size=size,
        sku="RYU-SHOES-BLACK-M",
    )

    duplicate = ProductVariant(
        product=product,
        color=color,
        size=size,
        sku="DIFFERENT-SKU",
    )

    with pytest.raises(ValidationError):
        duplicate.full_clean()


@pytest.mark.django_db
def test_product_price_cannot_be_negative(category):
    product = Product(
        category=category,
        name="Invalid product",
        slug="invalid-product",
        description="Invalid product used for testing.",
        base_price=Decimal("-1.00"),
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_product_can_have_only_one_primary_image(product):
    ProductImage.objects.create(
        product=product,
        image="catalog/products/primary.jpg",
        is_primary=True,
    )

    second_primary_image = ProductImage(
        product=product,
        image="catalog/products/second.jpg",
        is_primary=True,
    )

    with pytest.raises(ValidationError):
        second_primary_image.full_clean()