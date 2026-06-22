import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm, RegisterForm, JuegoForm
from django.http import HttpResponse
from .models import Juego
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

def base(request):
    juegos = Juego.objects.all()[:20]  # mostrar algunos en home
    return render(request, 'base.html', {'juegos': juegos})


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
                return redirect('base')
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
    auth_logout(request)
    return redirect('base')

#-----------------------------------------
def importar_juegos_gamesdb(request):
    if request.method != "POST":
        return redirect("lista_juegos")

    api_key = settings.GAMESDB_API_KEY

    if not api_key:
        messages.error(request, "No se encontró GAMESDB_API_KEY en el .env")
        return redirect("lista_juegos")

    busquedas = [
        "Mario",
        "Zelda",
        "FIFA",
        "Sonic",
        "Pokémon",
        "Resident Evil",
        "Need for Speed",
        "Final Fantasy",
        "Call of Duty",
        "GTA"
    ]

    total_guardados = 0

    try:
        for termino in busquedas:
            url = "https://api.thegamesdb.net/v1.1/Games/ByGameName"
            params = {
                "apikey": api_key,
                "name": termino
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            juegos_api = data.get("data", {}).get("games", [])

            for juego_api in juegos_api:
                game_id = juego_api.get("id")
                nombre = juego_api.get("game_title", "").strip()
                plataforma = juego_api.get("platform", "")
                resumen = juego_api.get("overview", "")

                fecha_lanzamiento = None
                fecha_raw = juego_api.get("release_date")
                if fecha_raw:
                    try:
                        fecha_lanzamiento = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
                    except ValueError:
                        pass

                if not nombre:
                    continue

                _, creado = Juego.objects.get_or_create(
                    gamesdb_id=game_id,
                    defaults={
                        "nombre": nombre,
                        "plataforma": str(plataforma) if plataforma else "",
                        "resumen": resumen or "",
                        "fecha_lanzamiento": fecha_lanzamiento,
                    }
                )

                if creado:
                    total_guardados += 1

        messages.success(request, f"Importación completada. Se guardaron {total_guardados} juegos.")
        return redirect("lista_juegos")

    except requests.RequestException as e:
        messages.error(request, f"Error al importar juegos: {e}")
        return redirect("lista_juegos")
    if request.method != "POST":
        return redirect("lista_juegos")

    api_key = settings.GAMESDB_API_KEY

    if not api_key:
        messages.error(request, "No se encontró GAMESDB_API_KEY en el .env")
        return redirect("lista_juegos")

    # Ejemplo: importamos por nombre genérico para traer muchos
    # después si querés lo mejoramos para importar por plataforma
    url = "https://api.thegamesdb.net/v1.1/Games/ByGameName"
    params = {
        "apikey": api_key,
        "name": "Mario"   # después esto lo podemos cambiar por otra estrategia
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        juegos_api = data.get("data", {}).get("games", [])

        if not juegos_api:
            messages.warning(request, "No se encontraron juegos para importar.")
            return redirect("lista_juegos")

        guardados = 0

        for juego_api in juegos_api:
            game_id = juego_api.get("id")
            nombre = juego_api.get("game_title", "").strip()
            plataforma = juego_api.get("platform", "")
            resumen = juego_api.get("overview", "")

            fecha_lanzamiento = None
            fecha_raw = juego_api.get("release_date")
            if fecha_raw:
                try:
                    fecha_lanzamiento = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
                except ValueError:
                    fecha_lanzamiento = None

            if not nombre:
                continue

            _, creado = Juego.objects.get_or_create(
                gamesdb_id=game_id,
                defaults={
                    "nombre": nombre,
                    "plataforma": str(plataforma) if plataforma else "",
                    "resumen": resumen or "",
                    "fecha_lanzamiento": fecha_lanzamiento,
                }
            )

            if creado:
                guardados += 1

        messages.success(request, f"Importación terminada. Juegos nuevos guardados: {guardados}")
        return redirect("lista_juegos")

    except requests.RequestException as e:
        messages.error(request, f"Error al conectar con TheGamesDB: {e}")
        return redirect("lista_juegos")

def lista_juegos(request):
    juegos = Juego.objects.all().order_by('nombre')
    return render(request, 'juegos/lista_juegos.html', {'juegos': juegos})


def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    return render(request, 'juegos/detalle_juego.html', {'juego': juego})


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


def borrar_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    if request.method == 'POST':
        juego.delete()
        return redirect('lista_juegos')

    return render(request, 'juegos/borrar_juego.html', {'juego': juego})