from django.db import models


class Product(models.Model):
    """Model definition for Product."""

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="products"
    )
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


class ProductImage(models.Model):
    """Model definition for ProductImage."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product")

    class Meta:
        """Meta definition for ProductImage."""

        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        """Unicode representation of ProductImage."""
        return self.product.name
