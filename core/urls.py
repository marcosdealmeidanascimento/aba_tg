from django.urls import path, include
from rest_framework import routers
from core.views.auth_views import MyProfileView, RegistroView
from core.views.paciente_views import PacienteViewSet
from core.views.profissional_views import (
    CompletarProfissionalView,
    ProfissionalPerfilView,
    )
from core.views.responsavel_views import (
     CompletarResponsavelView,
     ResponsavelPerfilView
)

# Routers de ViewSets
router = routers.DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')

urlpatterns = [
     # Me
     path('me/', MyProfileView.as_view(), name='meu_perfil'),

     # Rotas de Autenticação
     path('auth/register/', RegistroView.as_view(), name='auth_register'),

     # Rotas para Profissionais
     path('perfil/profissional/completar/',
          CompletarProfissionalView.as_view(),
          name='completar_profissional'),
     path('perfil/profissional/<pk>/', ProfissionalPerfilView.as_view(),
          name='perfil_profissional'),

     # Rotas para Responsável
     path('perfil/responsavel/completar/', CompletarResponsavelView.as_view(),
          name='completar_responavel'),
     path('perfil/responsavel/<pk>/', ResponsavelPerfilView.as_view(),
          name='perfil_responavel'),

     # Rotas para outros endpoints
     path('', include(router.urls)),
]
