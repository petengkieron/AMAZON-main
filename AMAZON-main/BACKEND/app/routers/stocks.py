from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models.stock import Stock
from ..models.product import Product
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def stock_list_view(request):
    if request.method == "GET":
        stocks = Stock.objects.all()
        return JsonResponse(list(stocks.values()), safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=data['product_id'])
            stock = Stock.objects.create(
                product=product,
                quantity=data['quantity'],
                store_name=data['store_name']
            )
            return JsonResponse({
                'id': stock.id,
                'product': stock.product.name,
                'quantity': stock.quantity,
                'store_name': stock.store_name
            }, status=201)
        except (KeyError, json.JSONDecodeError, Product.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def stock_detail_view(request, stock_id):
    try:
        stock = Stock.objects.get(id=stock_id)
    except Stock.DoesNotExist:
        return JsonResponse({'error': 'Stock not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': stock.id,
            'product': stock.product.name,
            'quantity': stock.quantity,
            'store_name': stock.store_name
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            stock.quantity = data.get('quantity', stock.quantity)
            stock.store_name = data.get('store_name', stock.store_name)
            stock.save()
            return JsonResponse({
                'id': stock.id,
                'product': stock.product.name,
                'quantity': stock.quantity,
                'store_name': stock.store_name
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)

    elif request.method == "DELETE":
        stock.delete()
        return JsonResponse({}, status=204)
