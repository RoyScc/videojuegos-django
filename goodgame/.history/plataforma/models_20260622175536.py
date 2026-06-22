from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="juegos"
    )
    gamesdb_id = models.IntegerField(unique=True, null=True, blank=True)
    plataforma = models.CharField(max_length=255, blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    imagen = models.URLField(blank=True, null=True)

    # para la parte “tienda”
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class CarritoItem(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item de carrito"
        verbose_name_plural = "Items de carrito"
        unique_together = ("usuario", "juego")
        ordering = ["-fecha_agregado"]

    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre} x{self.cantidad}"

    @property
    def subtotal(self):
        return self.juego.precio * self.cantidad


class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="items"
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item de pedido"
        verbose_name_plural = "Items de pedido"

    def __str__(self):
        return f"{self.juego.nombre} x{self.cantidad}"

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad