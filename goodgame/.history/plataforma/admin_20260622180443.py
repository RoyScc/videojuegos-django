from django.contrib import admin
from .models import Categoria, Juego, CarritoItem, Pedido, PedidoItem


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


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

class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "juego", "cantidad", "fecha_agregado")
    search_fields = ("usuario__username", "juego__nombre")
    list_filter = ("fecha_agregado",)
    ordering = ("-fecha_agregado",)


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "estado", "total")
    search_fields = ("usuario__username",)
    list_filter = ("estado", "fecha")
    ordering = ("-fecha",)
    inlines = [PedidoItemInline]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Juego, JuegoAdmin)
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(Pedido, PedidoAdmin)