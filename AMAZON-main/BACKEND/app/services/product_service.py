from ..models.product import Product

def list_products():
    try:
        products = Product.objects.all()
        return products
    except Exception as e:
        return []

def get_product_by_id(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return product
    except Product.DoesNotExist:
        return None
