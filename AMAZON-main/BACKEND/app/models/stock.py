from django.db import models
from django.core.validators import MinValueValidator

class Stock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    store_name = models.CharField(max_length=255, db_index=True)
    last_restock_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'store_name']
        
    def __str__(self):
        return f"{self.store_name}: {self.product.name} ({self.quantity})"

    def is_low_stock(self):
        return self.quantity < 10
