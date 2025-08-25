# Crie este arquivo dentro da sua pasta core/
from django.urls import path, include
from rest_framework import routers
from core.views.auth_views import DadosProfissionalView, RegistroView

# Routers de ViewSets
router = routers.DefaultRouter()
# router.register(r'usuarios', UsuarioViewSet) # Exemplo de rota

urlpatterns = [
    # Rotas de Autenticação
    path('auth/register/', RegistroView.as_view(), name='auth_register'),

    # Rotas para Profissionais
    path('profissional/dados/', DadosProfissionalView.as_view(), name='profissional_dados'),

    # Rotas para outros endpoints
    path('', include(router.urls)),
]