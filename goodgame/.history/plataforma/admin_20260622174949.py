from django.contrib import admin
from .models import Juego


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "gamesdb_id",
        "plataforma",
        "fecha_lanzamiento",
    )

    search_fields = (
        "nombre",
        "plataforma",
        "gamesdb_id",
    )

    list_filter = (
        "plataforma",
        "fecha_lanzamiento",
    )

    ordering = ("nombre",)