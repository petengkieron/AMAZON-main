from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, get_user_model
from ..services.auth_service import authenticate_user
import json

User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body)
    user = authenticate_user(data.get('username'), data.get('password'))
    
    if user:
        login(request, user)
        return JsonResponse({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            phone_number=data.get('phone_number', ''),
            address=data.get('address', '')
        )
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=201)
    except KeyError:
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
