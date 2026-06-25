from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado


class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado

    list_display = ("username", "email", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("username",)


admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)