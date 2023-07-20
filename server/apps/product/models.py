from django.db import models

from server.apps.core.models import BaseModel


class Product(BaseModel):
    """Model definition for Product."""

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="products"
    )
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.IntegerField(default=0)
    is_new = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        """Meta definition for Product."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """Unicode representation of Product."""
        
        return self.name


class ProductImage(BaseModel):
    """Model definition for ProductImage."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product")

    class Meta(BaseModel.Meta):
        """Meta definition for ProductImage."""

        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        """Unicode representation of ProductImage."""

        return self.product.name


class ProductWeight(BaseModel):
    """Model definition for ProductWeight."""

    person_count = models.IntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta(BaseModel.Meta):
        """Meta definition for ProductWeight."""

        verbose_name = "ProductWeight"
        verbose_name_plural = "ProductWeights"

    def __str__(self):
        """Unicode representation of ProductWeight."""

        return f"{self.person_count} - {self.weight}"
