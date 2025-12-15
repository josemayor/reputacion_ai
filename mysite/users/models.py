from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    # La longitud del hash SHA-256 es siempre de 256 bits,
    # lo que equivale a una cadena de 64 caracteres

    def __str__(self):
        return self.username[:25]
