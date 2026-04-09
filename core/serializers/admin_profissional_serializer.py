from rest_framework import serializers
from core.models.profissional import Profissional
from core.serializers.profissional_serializer import ProfissionalSerializer


class AdminProfissionalListSerializer(ProfissionalSerializer):
    class Meta(ProfissionalSerializer.Meta):
        fields = ProfissionalSerializer.Meta.fields + [
            'status_validacao',
            'crp_validado',
            'historico_criminal_aprovado',
            'notas_admin',
        ]


class AdminProfissionalDetailSerializer(AdminProfissionalListSerializer):
    """Alias mantido para semântica — campos de documentos já herdados do ProfissionalSerializer."""
    pass


class ValidacaoProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = [
            'status_validacao',
            'crp_validado',
            'historico_criminal_aprovado',
            'notas_admin',
        ]
