from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import UsuarioPersonalizado

# Create your views here.

# def registrarse(request):
#     if request.method == 'POST':
#         form = UsuarioPersonalizadoForm(request.POST)
#         if form.is_valid():
#             usuario = form.save()
#             login(request, usuario)
#             return redirect('plataforma:home')
    
#     else:
#         form = UsuarioPersonalizadoForm()
#     return render(request, 'usuarios/registrarse.html', {'form': form})