from decimal import Decimal

import pytest

from apps.catalog.models import Category, Color, Product, Size


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Shoes",
        slug="shoes",
    )


@pytest.fixture
def color(db):
    return Color.objects.create(
        name="Black",
        slug="black",
        hex_code="#000000",
    )


@pytest.fixture
def size(db):
    return Size.objects.create(
        name="Medium",
        code="M",
        sort_order=1,
    )


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        name="Ryu Training Shoes",
        slug="ryu-training-shoes",
        description="Training shoes for everyday workouts.",
        base_price=Decimal("299.99"),
    )