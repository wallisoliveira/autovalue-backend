from rest_framework import serializers # type: ignore
from .models import Veiculo, AvaliacaoPreditiva, WorkflowEtapa, WorkflowItem

# Serializer para o Módulo de Precificação
class AvaliacaoPreditivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliacaoPreditiva
        fields = '__all__'

# Serializer para o Módulo de Veículos
class VeiculoSerializer(serializers.ModelSerializer):
    avaliacao_preditiva = AvaliacaoPreditivaSerializer(read_only=True) 

    # Adicionamos validadores explícitos para forçar a aceitação de Inteiros
    ano = serializers.IntegerField(required=True)
    quilometragem = serializers.IntegerField(required=True)

    class Meta:
        model = Veiculo
        # Usamos '__all__' para incluir todos os campos (status)
        fields = '__all__' 
        read_only_fields = ('data_compra', 'data_venda', 'avaliacao_preditiva',) 
        extra_kwargs = {
            # Garante que o avaliador (ForeignKey) é opcional.
            'avaliador': {'required': False, 'allow_null': True}, 
            'data_entrada': {'required': False, 'read_only': True},
            'cor': {'required': False, 'allow_blank': True},
        }
        
# --- SERIALIZERS FALTANTES (KANBAN) ---

class WorkflowEtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowEtapa
        fields = '__all__'

class WorkflowItemSerializer(serializers.ModelSerializer):
    veiculo_info = VeiculoSerializer(source='veiculo', read_only=True)
    etapa_nome = serializers.CharField(source='etapa_atual.nome', read_only=True)

    class Meta:
        model = WorkflowItem
        fields = ('id', 'veiculo', 'veiculo_info', 'etapa_atual', 'etapa_nome', 
                  'tmv_prioridade', 'data_inicio_etapa', 'responsavel')
        read_only_fields = ('veiculo_info', 'etapa_nome')