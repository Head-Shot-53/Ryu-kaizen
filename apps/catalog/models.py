from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/categories/", blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        if self.pk and self.parent_id == self.pk:
            raise ValidationError(
                {"parent": "A category cannot be its own parent."}
            )


class Collection(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/collections/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValidationError(
                {
                    "ends_at": (
                        "The collection end date must be later "
                        "than its start date."
                    )
                }
            )


class Color(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    hex_code = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^#[0-9A-Fa-f]{6}$",
                message="Enter a valid HEX color, for example #000000."
            )
        ],
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self) -> str:
        return self.name


class Size(TimeStampedModel):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=20, unique=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self) -> str:
        return self.code


class Product(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    class Audience(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        KIDS = "kids", "Kids"
        UNISEX = "unisex", "Unisex"

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    collections = models.ManyToManyField(Collection, related_name="products", blank=True)
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    audience = models.CharField(max_length=20, choices=Audience.choices, default=Audience.UNISEX)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product"
        verbose_name_plural = "Products"
        constraints = [
            models.CheckConstraint(
                condition=Q(base_price__gte=0),
                name="catalog_product_price_gte_zero"
            ),
        ]
        indexes = [
            models.Index(
                fields=("status", "is_featured"),
                name="cat_prod_status_feat_idx"
            )
        ]

    def __str__(self) -> str:
        return self.name


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.ForeignKey(Color,on_delete=models.PROTECT, related_name="product_variants")
    size = models.ForeignKey(Size, on_delete=models.PROTECT, related_name="product_variants")
    sku = models.CharField(max_length=80,unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Leave empty to use the product base price."
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("product", "color", "size")
        verbose_name = "Product variant"
        verbose_name_plural = "Product variants"
        constraints = [
            models.UniqueConstraint(
                fields=("product", "color", "size"),
                name="catalog_unique_product_color_size"
            ),
            models.CheckConstraint(
                condition=Q(price__isnull=True) | Q(price__gte=0),
                name="catalog_variant_price_gte_zero"
            ),
            models.CheckConstraint(
                condition=Q(stock_quantity__gte=0),
                name="catalog_variant_stock_gte_zero"
            ),
        ]
        indexes = [
            models.Index(
                fields=("product", "is_active"),
                name="cat_var_product_active_idx"
            )
        ]

    def __str__(self) -> str:
        return f"{self.product.name} — {self.color.name} — {self.size.code}"

    @property
    def effective_price(self):
        if self.price is not None:
            return self.price

        return self.product.base_price


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        related_name="product_images",
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to="catalog/products/")
    alt_text = models.CharField(max_length=180, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "created_at")
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        constraints = [
            models.UniqueConstraint(
                fields=("product",),
                condition=Q(is_primary=True),
                name="catalog_one_primary_image_per_product",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product.name} image #{self.sort_order}"