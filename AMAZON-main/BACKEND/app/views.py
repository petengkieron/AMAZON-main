# Contenu actuel de views.py 
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API fonctionne !',
        'products': [
            {'id': 1, 'name': 'Test Product', 'price': 99.99}
        ]
    }) 