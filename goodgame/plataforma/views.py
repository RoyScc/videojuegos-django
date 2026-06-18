from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')
    

def login(request):
    if request.method == 'POST':
        # Procesar el form de login
        pass
    else:
        # Mostrar el form de login
        pass

    return render(request, 'registration/login.html')