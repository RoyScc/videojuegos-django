from .models import CarritoItem


def mini_carrito(request):
    cantidad_carrito = 0

    if request.user.is_authenticated:
        cantidad_carrito = CarritoItem.objects.filter(
            usuario=request.user
        ).count()

    return {
        "cantidad_carrito": cantidad_carrito
    }