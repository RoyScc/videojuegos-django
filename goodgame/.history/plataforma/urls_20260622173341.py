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
]