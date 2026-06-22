from django.db import models

class Juego(models.Model):
    nombre = models.CharField(max_length=255)
    gamesdb_id = models.IntegerField(unique=True, null=True, blank=True)
    plataforma = models.CharField(max_length=255, blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre