from django.contrib import admin
from .models import Juego


class JuegoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "plataforma",
        "fecha_lanzamiento",
        "gamesdb_id",
        "tiene_imagen",
        "precio",
    )

    search_fields = (
        "nombre",
        "plataforma",
        "resumen",
    )

    list_filter = (
        "plataforma",
        "fecha_lanzamiento",
    )

    ordering = ("nombre",)

    def tiene_imagen(self, obj):
        return bool(obj.imagen)

    tiene_imagen.boolean = True
    tiene_imagen.short_description = "Imagen"


admin.site.register(Juego, JuegoAdmin)