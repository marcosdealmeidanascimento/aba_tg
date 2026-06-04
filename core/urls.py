from django.urls import path, include
from rest_framework import routers
from core.views.atividade_views import AtividadeViewSet
from core.views.auditoria_views import AuditoriaViewSet
from core.views.auth_views import MyProfileView, RegistroView
from core.views.execucao_atividade_views import ExecucaoAtividadeViewSet
from core.views.modulo_views import ModuloViewSet
from core.views.nivel_views import NivelViewSet
from core.views.paciente_views import PacienteViewSet
from core.views.pedido_vinculo_views import PedidoVinculoViewSet
from core.views.profissional_views import (
    CompletarProfissionalView,
    ProfissionalPerfilView,
    ProfissionalListView,
    )
from core.views.responsavel_views import (
     CompletarResponsavelView,
     ResponsavelPerfilView
)
from core.views.diagnostico_views import (   
     DiagnosticoViewSet,
     GetDiagnosticoByPacienteView
)
from core.views.sessao_views import GetSessoesByPacienteView, SessaoViewSet, FecharSessaoAPIView
from core.views.pedido_agendamento_views import PedidoAgendamentoViewSet
from core.views.disponibilidade_views import DisponibilidadeProfissionalViewSet
from core.views.admin_profissional_views import (
    AdminProfissionalListView,
    AdminProfissionalDetailView,
    AdminValidacaoProfissionalView,
)
from core.views.admin_responsavel_views import AdminResponsavelListView
from core.views.ticket_views import (
    TicketListCreateView,
    TicketDetailView,
    ResponderTicketView,
)
from core.views.import_views import ImportXMLView

# Routers de ViewSets
router = routers.DefaultRouter()
router.register(r"auditorias", AuditoriaViewSet, basename="auditoria")
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'diagnosticos', DiagnosticoViewSet, basename='diagnostico')
router.register(r'sessoes', SessaoViewSet, basename='sessao')
router.register(r'modulos', ModuloViewSet, basename='modulo')
router.register(r'execucao-atividades', ExecucaoAtividadeViewSet, basename='execucao')
router.register(r'pedidos-vinculo', PedidoVinculoViewSet, basename='pedido-vinculo')
router.register(r'atividades', AtividadeViewSet, basename='atividade')
router.register(r'niveis', NivelViewSet, basename='nivel')
router.register(r'pedidos-agendamento', PedidoAgendamentoViewSet, basename='pedido-agendamento')
router.register(r'disponibilidades', DisponibilidadeProfissionalViewSet, basename='disponibilidade')

urlpatterns = [
     # Me
     path('me/', MyProfileView.as_view(), name='meu_perfil'),

     # Rotas de Autenticação
     path('auth/register/', RegistroView.as_view(), name='auth_register'),
     path('auth/register/<int:pk>/', RegistroView.as_view(), name='auth_register_detail'),

     # Rotas para Profissionais
     path('perfil/profissional/completar/',
          CompletarProfissionalView.as_view(),
          name='completar_profissional'),
     path('perfil/profissional/<pk>/', ProfissionalPerfilView.as_view(),
          name='perfil_profissional'),
     path('profissionais/', ProfissionalListView.as_view(), name='profissionais'),

     # Rotas para Responsável
     path('perfil/responsavel/completar/', CompletarResponsavelView.as_view(),
          name='completar_responavel'),
     path('perfil/responsavel/<pk>/', ResponsavelPerfilView.as_view(),
          name='perfil_responavel'),

     # Rotas para Diagnostico
     path('diagnosticos/paciente/<int:paciente_id>/',
          GetDiagnosticoByPacienteView.as_view(),
          name='diagnostico_paciente'),

     # Rotas para Sessao
     path('sessoes/fechar/<int:pk>/', FecharSessaoAPIView.as_view(), name='fechar_sessao'),
     path('sessoes/paciente/<int:paciente_id>/', GetSessoesByPacienteView.as_view(), name='sessoes_paciente'),

     # Rotas de Suporte
     path('suporte/tickets/', TicketListCreateView.as_view(), name='ticket_list_create'),
     path('suporte/tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
     path('suporte/tickets/<int:pk>/responder/', ResponderTicketView.as_view(), name='ticket_responder'),

     # Rotas Admin — Importação XML
     path('admin/import/xml/', ImportXMLView.as_view(), name='import_xml'),

     # Rotas Admin — Profissionais
     path('admin/profissionais/', AdminProfissionalListView.as_view(), name='admin_profissional_list'),
     path('admin/responsaveis/', AdminResponsavelListView.as_view(), name='admin_responsavel_list'),
     path('admin/profissionais/<int:pk>/', AdminProfissionalDetailView.as_view(), name='admin_profissional_detail'),
     path('admin/profissionais/<int:pk>/validacao/', AdminValidacaoProfissionalView.as_view(), name='admin_validacao_profissional'),

     # Rotas para outros endpoints
     path('', include(router.urls)),
]
