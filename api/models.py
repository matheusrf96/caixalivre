from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Seller(models.Model):
    full_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Purchase(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    seller = models.OneToOneField(Seller, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def commission(self):
        return False


class PurchaseProducts(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='products', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='purchase', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    commission = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
