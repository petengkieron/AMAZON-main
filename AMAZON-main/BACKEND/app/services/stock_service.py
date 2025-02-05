from ..models.stock import Stock
from django.db.models import F

def update_stock_quantity(stock_id, quantity):
    try:
        stock = Stock.objects.get(id=stock_id)
        stock.quantity = F('quantity') + quantity
        stock.save()
        stock.refresh_from_db()
        return stock
    except Stock.DoesNotExist:
        return None

def get_low_stock_products():
    return Stock.objects.filter(quantity__lt=10)

def list_stocks():
    return Stock.objects.all()

def get_stock_by_id(stock_id):
    try:
        return Stock.objects.get(id=stock_id)
    except Stock.DoesNotExist:
        return None
