from django.db import models
from django.conf import settings


class Juego(models.Model):
    nombre = models.CharField(max_length=255)
    gamesdb_id = models.IntegerField(unique=True, null=True, blank=True)
    plataforma = models.CharField(max_length=255, blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    imagen = models.URLField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre


class CarritoItem(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)


class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)