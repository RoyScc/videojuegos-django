import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm, RegisterForm, JuegoForm
from django.http import HttpResponse
from .models import Juego

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
def importar_juegos_steam(request):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS CODE:", response.status_code)
        print("CONTENT TYPE:", response.headers.get("Content-Type"))
        print("PRIMEROS 500 CHARS:")
        print(response.text[:500])

        # si la respuesta no es 200, mostramos error
        if response.status_code != 200:
            return HttpResponse(
                f"Steam devolvió error {response.status_code}<br><pre>{response.text[:500]}</pre>"
            )

        # intentamos convertir a json
        try:
            data = response.json()
        except ValueError:
            return HttpResponse(
                f"La respuesta no vino en JSON.<br><br><pre>{response.text[:1000]}</pre>"
            )

        apps = data.get("applist", {}).get("apps", [])

        if not apps:
            return HttpResponse("No se encontraron apps en la respuesta de Steam.")

        # limitamos para no meter 100k juegos
        apps = apps[:100]

        guardados = 0
        for app in apps:
            appid = app.get("appid")
            nombre = app.get("name", "").strip()

            if not nombre:
                continue

            _, creado = Juego.objects.get_or_create(
                steam_appid=appid,
                defaults={"nombre": nombre}
            )

            if creado:
                guardados += 1

        return HttpResponse(f"Importación terminada. Juegos guardados: {guardados}")

    except requests.RequestException as e:
        return HttpResponse(f"Error al conectar con Steam: {e}")


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