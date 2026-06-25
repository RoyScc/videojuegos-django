from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    #path('', views.base, name='base'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("juegos/importar/", views.importar_juegos_gamesdb, name="importar_juegos_gamesdb"),
    path("juegos/importar-imagenes/", views.importar_imagenes_gamesdb, name="importar_imagenes_gamesdb"),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('juegos/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    path('juegos/<int:juego_id>/editar/', views.editar_juego, name='editar_juego'),
    path('juegos/<int:juego_id>/borrar/', views.borrar_juego, name='borrar_juego'),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:juego_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/quitar/<int:item_id>/", views.quitar_del_carrito, name="quitar_del_carrito"),
    path("carrito/comprar-ahora/<int:juego_id>/", views.comprar_ahora, name="comprar_ahora"),
    path("carrito/cancelar/", views.cancelar_compra, name="cancelar_compra"),
    path("carrito/comprar/", views.comprar_carrito, name="comprar_carrito"),
    path("compra-exitosa/", views.compra_exitosa, name="compra_exitosa"),
    path("biblioteca/", views.biblioteca, name="biblioteca"),
    
]