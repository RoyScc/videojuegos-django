import requests
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import LoginForm, RegisterForm, JuegoForm
from django.http import HttpResponse
from .models import Juego, CarritoItem, BibliotecaItem
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def base(request):
    juegos = Juego.objects.all()[:20]  # mostrar algunos en home
    return render(request, 'base.html', {'juegos': juegos})

def inicio(request):
    juegos = Juego.objects.all().order_by("nombre")

    juegos_carrousel = juegos[:5]
    resto_juegos = juegos[5:]

    paginator = Paginator(resto_juegos, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inicio.html", {
        "juegos_carrousel": juegos_carrousel,
        "page_obj": page_obj,
    })

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos.')

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # lo loguea automáticamente al registrarse
            return redirect('base')

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

#Agregado de vistas para la gestión de juegos

def lista_juegos(request):
    juegos = Juego.objects.all().order_by("nombre")
    mostrar_boton_importar = not juegos.exists()

    return render(request, "juegos/lista_juegos.html", {
        "juegos": juegos,
        "mostrar_boton_importar": mostrar_boton_importar
    })


def importar_juegos_gamesdb(request):
    if request.method != "POST":
        return redirect("lista_juegos")

    api_key = settings.GAMESDB_API_KEY

    if not api_key:
        messages.error(request, "No se encontró GAMESDB_API_KEY en el archivo .env")
        return redirect("lista_juegos")

    busquedas = [
        "Mario",
        "Zelda",
        "FIFA",
        "Sonic",
        "Pokemon",
        "Resident Evil",
        "Need for Speed",
        "Final Fantasy",
        "Call of Duty",
        "GTA"
    ]

    total_guardados = 0
    total_actualizados = 0

    try:
        for termino in busquedas:
            url = "https://api.thegamesdb.net/v1.1/Games/ByGameName"
            params = {
                "apikey": api_key,
                "name": termino,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            juegos_api = data.get("data", {}).get("games", [])
            include = data.get("include", {})
            boxart_data = include.get("boxart", {})
            base_url = data.get("include", {}).get("boxart", {})
            base_img_url = data.get("pages", {})  
            imagen_base = None
            if "base_url" in data:
                imagen_base = data["base_url"].get("medium") or data["base_url"].get("original")
            elif "images" in data:
                imagen_base = data["images"].get("base_url", {}).get("medium")

            for juego_api in juegos_api:
                game_id = juego_api.get("id")
                nombre = (juego_api.get("game_title") or "").strip()

                if not nombre or not game_id:
                    continue

                plataforma = juego_api.get("platform")
                plataforma = str(plataforma) if plataforma else ""

                resumen = juego_api.get("overview") or ""

                fecha_lanzamiento = None
                fecha_raw = juego_api.get("release_date")
                if fecha_raw:
                    try:
                        fecha_lanzamiento = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
                    except ValueError:
                        fecha_lanzamiento = None

                anio_actual = date.today().year

                if fecha_lanzamiento:
                    edad = anio_actual - fecha_lanzamiento.year

                    if edad <= 2:
                        precio = random.randint(7000, 10000)
                    elif edad <= 5:
                        precio = random.randint(4000, 7000)
                    else:
                        precio = random.randint(1000, 4000)
                else:
                    precio = random.randint(1000, 5000)
                    
                imagen = ""

                game_boxarts = boxart_data.get(str(game_id), []) or boxart_data.get(game_id, [])

                if game_boxarts:
                    portada = None

                    for img in game_boxarts:
                        side = (img.get("side") or "").lower()
                        img_type = (img.get("type") or "").lower()

                        if side == "front":
                            portada = img
                            break
                        if img_type == "boxart":
                            portada = img

                    if not portada:
                        portada = game_boxarts[0]

                    filename = portada.get("filename")
                    if filename:
                        if imagen_base:
                            imagen = f"{imagen_base}{filename}"
                        else:
                            imagen = f"https://cdn.thegamesdb.net/images/medium/{filename}"

                juego, creado = Juego.objects.get_or_create(
                    gamesdb_id=game_id,
                    defaults={
                        "nombre": nombre,
                        "plataforma": plataforma,
                        "fecha_lanzamiento": fecha_lanzamiento,
                        "resumen": resumen,
                        "imagen": imagen,
                        "precio": precio,
                    }
                )

                if creado:
                    total_guardados += 1
                else:
                    actualizado = False

                    if not juego.plataforma and plataforma:
                        juego.plataforma = plataforma
                        actualizado = True

                    if not juego.fecha_lanzamiento and fecha_lanzamiento:
                        juego.fecha_lanzamiento = fecha_lanzamiento
                        actualizado = True

                    if not juego.resumen and resumen:
                        juego.resumen = resumen
                        actualizado = True

                    if not juego.imagen and imagen:
                        juego.imagen = imagen
                        actualizado = True

                    if actualizado:
                        juego.save()
                        total_actualizados += 1

        messages.success(
            request,
            f"Importación completada. Nuevos: {total_guardados}. Actualizados: {total_actualizados}."
        )
        return redirect("lista_juegos")

    except requests.RequestException as e:
        messages.error(request, f"Error al conectar con TheGamesDB: {e}")
        return redirect("lista_juegos")

@staff_member_required
def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    return render(request, 'juegos/detalle_juego.html', {'juego': juego})

@staff_member_required
def editar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('detalle_juego', juego_id=juego.id)
    else:
        form = JuegoForm(instance=juego)

    return render(request, 'juegos/editar_juego.html', {
        'form': form,
        'juego': juego
    })

@staff_member_required
def borrar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    if request.method == 'POST':
        juego.delete()
        return redirect('lista_juegos')

    return render(request, 'juegos/borrar_juego.html', {'juego': juego})

#Agregado de importación de imágenes desde TheGamesDB
def importar_imagenes_gamesdb(request):
    if request.method != "POST":
        return redirect("lista_juegos")

    api_key = settings.GAMESDB_API_KEY

    if not api_key:
        messages.error(request, "No se encontró GAMESDB_API_KEY en el archivo .env")
        return redirect("lista_juegos")

    juegos_sin_imagen = Juego.objects.filter(
        gamesdb_id__isnull=False).filter(Q(imagen__isnull=True) | Q(imagen="")
    )

    actualizados = 0
    sin_imagen = 0

    try:
        for juego in juegos_sin_imagen:
            url = "https://api.thegamesdb.net/v1/Games/Images"
            params = {
                "apikey": api_key,
                "games_id": juego.gamesdb_id,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            base_url = data.get("data", {}).get("base_url", {})
            imagen_base = (
                base_url.get("medium")
                or base_url.get("original")
                or "https://cdn.thegamesdb.net/images/medium/"
            )

            images_data = data.get("data", {}).get("images", {})
            game_images = images_data.get(str(juego.gamesdb_id), []) or images_data.get(juego.gamesdb_id, [])

            if not game_images:
                sin_imagen += 1
                continue

            portada = None

            for img in game_images:
                side = (img.get("side") or "").lower()
                img_type = (img.get("type") or "").lower()

                if side == "front":
                    portada = img
                    break
                if img_type == "boxart":
                    portada = img

            if not portada:
                portada = game_images[0]

            filename = portada.get("filename")
            if not filename:
                sin_imagen += 1
                continue

            juego.imagen = f"{imagen_base}{filename}"
            juego.save()
            actualizados += 1

        messages.success(
            request,
            f"Imágenes importadas. Juegos actualizados: {actualizados}. Sin imagen encontrada: {sin_imagen}."
        )
        return redirect("lista_juegos")

    except requests.RequestException as e:
        messages.error(request, f"Error al importar imágenes desde TheGamesDB: {e}")
        return redirect("lista_juegos")
    

#Agregado de carrito de compras
@login_required
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    CarritoItem.objects.get_or_create(
        usuario=request.user,
        juego=juego
    )

    messages.success(request, f"{juego.nombre} fue agregado al carrito.")
    return redirect("ver_carrito")


@login_required
def ver_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user).select_related("juego")

    total = sum(item.juego.precio for item in items)

    return render(request, "carrito/ver_carrito.html", {
        "items": items,
        "total": total
    })


@login_required
def quitar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Juego eliminado del carrito.")

    return redirect("ver_carrito")


@login_required
def cancelar_compra(request):
    if request.method == "POST":
        CarritoItem.objects.filter(usuario=request.user).delete()
        messages.info(request, "Compra cancelada.")

    return redirect("ver_carrito")


@login_required
def comprar_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)

    if not items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect("ver_carrito")

    if request.method == "POST":
        items.delete()
        return redirect("compra_exitosa")

    return redirect("ver_carrito")


@login_required
def compra_exitosa(request):
    return render(request, "carrito/compra_exitosa.html")

#Agregado de biblioteca de juegos

@login_required
def comprar_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)

    if not items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect("ver_carrito")

    if request.method == "POST":
        for item in items:
            BibliotecaItem.objects.get_or_create(
                usuario=request.user,
                juego=item.juego
            )

        items.delete()
        return redirect("compra_exitosa")

    return redirect("ver_carrito")

@login_required
def biblioteca(request):
    juegos = BibliotecaItem.objects.filter(
        usuario=request.user
    ).select_related("juego").order_by("-fecha_compra")

    return render(request, "biblioteca/biblioteca.html", {
        "juegos": juegos
    })