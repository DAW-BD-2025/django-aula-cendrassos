# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

from rest_framework import exceptions
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from aula.apps.alumnes.models import Alumne


class CustomJWTAuthentication(JWTAuthentication):
    """Retorna un JSON per l'error 401 si el token JWT no és vàlid o està caducat."""

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, TokenError):
            raise exceptions.AuthenticationFailed(
                {"error": ["Token invàlid o caducat"]}
            )


class EsUsuariDeLaAPI(permissions.BasePermission):
    """
    Només permet responsables vinculats a un alumne/a o alumnes majors de 18 anys.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        alumne_id = view.kwargs.get("alumne_id")
        if not alumne_id:
            return False

        try:
            alumne = Alumne.objects.get(id=int(alumne_id))
        except (TypeError, ValueError, Alumne.DoesNotExist):
            return False

        responsable = getattr(user, "responsable", None)
        alumne_pertany_a_responsable = (
            bool(responsable)
            and responsable.alumnes_associats.filter(id=alumne.id).exists()
        )

        edad = alumne.edat()
        alumne_es_major_de_18 = edad is not None and edad >= 18

        return alumne_pertany_a_responsable or alumne_es_major_de_18
