from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response
from core.models import ExecucaoAtividade
from core.serializers.execucao_atividade_serializer import ExecucaoAtividadeSerializer


class ExecucaoAtividadeViewSet(viewsets.ModelViewSet):
    queryset = ExecucaoAtividade.objects.all()
    serializer_class = ExecucaoAtividadeSerializer

    def get_queryset(self):
        queryset = ExecucaoAtividade.objects.all()
        paciente_id = self.request.query_params.get('pacienteId', None)
        sessao_id = self.request.query_params.get('sessaoId', None)
        if paciente_id is not None:
            queryset = queryset.filter(paciente_id=paciente_id)
        if sessao_id is not None:
            queryset = queryset.filter(sessao_id=sessao_id)
        return queryset

    @action(detail=False, methods=['get'])
    def resumo(self, request):
        paciente_id = request.query_params.get('pacienteId')
        sessao_id = request.query_params.get('sessaoId')

        queryset = self.get_queryset()

        if not paciente_id and not sessao_id:
            return Response({"error": "Informe pacienteId ou sessaoId"}, status=400)

        total_execucoes = queryset.count()

        if total_execucoes == 0:
            return Response({
                "total": 0,
                "stats": [],
                "message": "Nenhuma atividade executada neste contexto."
            })

        contagem = queryset.values('status').annotate(total=Count('status'))

        stats = []
        for item in contagem:
            status_key = item['status']
            quantidade = item['total']
            percentual = round((quantidade / total_execucoes) * 100, 2)

            label = dict(ExecucaoAtividade.STATUS_CHOICES).get(status_key, status_key)

            stats.append({
                "status": status_key,
                "label": label,
                "quantidade": quantidade,
                "percentual": f"{percentual}%"
            })

        return Response({
            "resumo_texto": f"Resumo de Desempenho (Total: {total_execucoes} atividades)",
            "total_geral": total_execucoes,
            "estatisticas": stats
        })
