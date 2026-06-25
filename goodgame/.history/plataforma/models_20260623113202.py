from django.db import models
from django.conf import settings


class Juego(models.Model):
    nombre = models.CharField(max_length=255)
    gamesdb_id = models.IntegerField(unique=True, null=True, blank=True)
    plataforma = models.CharField(max_length=255, blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    imagen = models.URLField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    imagen_local = models.ImageField(upload_to="juegos/", blank=True, null=True)

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "juego")

    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre}"
    
class BibliotecaItem(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="biblioteca_items"
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name="biblioteca_items"
    )
    fecha_compra = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "juego")

    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre}"
    
