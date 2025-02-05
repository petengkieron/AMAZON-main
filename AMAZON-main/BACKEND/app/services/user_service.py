from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

User = get_user_model()

def create_user(prenom, nom, numero, password):
    if not all([prenom, nom, password]):
        raise ValidationError("Les champs prenom, nom et password sont obligatoires")
    
    with transaction.atomic():
        if User.objects.filter(numero=numero).exists():
            raise ValidationError("Ce numéro existe déjà")
            
        user = User.objects.create_user(
            username=numero,
            prenom=prenom,
            nom=nom,
            numero=numero,
            password=password
        )
        return user

def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

def update_user(user_id, **data):
    with transaction.atomic():
        user = get_user_by_id(user_id)
        if not user:
            raise ValidationError("Utilisateur non trouvé")
        
        if 'numero' in data and data['numero'] != user.numero:
            if User.objects.filter(numero=data['numero']).exists():
                raise ValidationError("Ce numéro existe déjà")
        
        for field, value in data.items():
            if field == 'password':
                user.set_password(value)
            elif hasattr(user, field):
                setattr(user, field, value)
        
        user.save()
        return user

def delete_user(user_id):
    with transaction.atomic():
        user = get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

def list_users():
    return User.objects.all()
