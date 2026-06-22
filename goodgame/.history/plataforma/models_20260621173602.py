from django.db import models

class Juego(models.Model):
    steam_appid = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} ({self.steam_appid})"