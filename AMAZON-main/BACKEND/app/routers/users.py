from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..services import user_service
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_list_view(request):
    if request.method == "GET":
        users = user_service.list_users()
        return JsonResponse([{
            'id': user.id,
            'prenom': user.prenom,
            'nom': user.nom,
            'numero': user.numero
        } for user in users], safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            user = user_service.create_user(
                prenom=data['prenom'],
                nom=data['nom'],
                numero=data['numero'],
                password=data['password']
            )
            return JsonResponse({
                'id': user.id,
                'prenom': user.prenom,
                'nom': user.nom,
                'numero': user.numero
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def user_detail_view(request, user_id):
    if request.method == "GET":
        user = user_service.get_user_by_id(user_id)
        if not user:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        return JsonResponse({
            'id': user.id,
            'prenom': user.prenom,
            'nom': user.nom,
            'numero': user.numero
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = user_service.update_user(user_id, **data)
            return JsonResponse({
                'id': user.id,
                'prenom': user.prenom,
                'nom': user.nom,
                'numero': user.numero
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == "DELETE":
        if user_service.delete_user(user_id):
            return JsonResponse({}, status=204)
        return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
