from django.urls import path
from .views import GenerarMultaView

from . import views

urlpatterns = [
    path('generar_multa/', GenerarMultaView.as_view(), name='generar_multa'),
]