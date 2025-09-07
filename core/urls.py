from django.urls import path, include
from rest_framework import routers
from core.views.auth_views import RegistroView
from core.views.profissional_views import CompletarProfissionalView
from core.views.responsavel_views import CompletarResponsavelView

# Routers de ViewSets
router = routers.DefaultRouter()
# router.register(r'usuarios', UsuarioViewSet) # Exemplo de rota

urlpatterns = [
    # Rotas de Autenticação
    path('auth/register/', RegistroView.as_view(), name='auth_register'),

    # Rotas para Profissionais
    path('perfil/profissional/completar/', CompletarProfissionalView.as_view(),
         name='completar_profissional'),

    # Rotas para Responsável
    path('perfil/responsavel/completar/', CompletarResponsavelView.as_view(),
         name='completar_responavel'),


    # Rotas para outros endpoints
    path('', include(router.urls)),
]