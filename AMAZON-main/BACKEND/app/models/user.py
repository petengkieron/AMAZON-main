from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    prenom = models.CharField(max_length=100, null=False)
    nom = models.CharField(max_length=100, null=False)
    numero = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        unique=True,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['prenom', 'nom']),
            models.Index(fields=['numero']),  # Correction de l'index
        ]
