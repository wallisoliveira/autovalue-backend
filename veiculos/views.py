from rest_framework import viewsets, status
from rest_framework.response import Response 
from .models import Veiculo, AvaliacaoPreditiva, WorkflowEtapa, WorkflowItem
from .serializers import VeiculoSerializer, AvaliacaoPreditivaSerializer, WorkflowEtapaSerializer, WorkflowItemSerializer
import random 
from django.shortcuts import get_object_or_404 # Útil, embora não seja usado diretamente no POST

# --- OUTROS VIEWSETS ---

class AvaliacaoPreditivaViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoPreditiva.objects.all()
    serializer_class = AvaliacaoPreditivaSerializer

class WorkflowEtapaViewSet(viewsets.ModelViewSet):
    queryset = WorkflowEtapa.objects.all().order_by('ordem')
    serializer_class = WorkflowEtapaSerializer

class WorkflowItemViewSet(viewsets.ModelViewSet):
    queryset = WorkflowItem.objects.all().order_by('tmv_prioridade')
    serializer_class = WorkflowItemSerializer
    filterset_fields = ['etapa_atual']

# --- VEICULO VIEWSET (CORRIGIDO PARA O CREATE/RETRIEVE) ---

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all().order_by('-data_entrada')
    serializer_class = VeiculoSerializer
    filterset_fields = ['status', 'marca']

    def perform_create(self, serializer):
        # 1. Salva o Veículo e Trata o Usuário (Avaliador)
        veiculo = serializer.save(
            avaliador=self.request.user if self.request.user.is_authenticated else None
        )

        # 2. SIMULAÇÃO DA IA E PRECIFICAÇÃO
        ano_carro = veiculo.ano
        simulacao_preco_base = 60000 + (2025 - ano_carro) * -5000
        simulacao_preco_final = round(simulacao_preco_base * (1 + random.uniform(-0.1, 0.1)), 2)
        simulacao_tmv = random.randint(20, 90)

        # 3. Cria a AvaliacaoPreditiva
        AvaliacaoPreditiva.objects.create(
            veiculo=veiculo,
            preco_maximo_compra=simulacao_preco_final,
            tmv_previsto_dias=simulacao_tmv,
            fipe_referencia=simulacao_preco_final * 1.15,
            mercado_medio_concorrencia=simulacao_preco_final * 1.05,
            margem_desejada=20 
        )
        
        # 4. Cria o item inicial no Workflow (Kanban)
        try:
            etapa_inicial = WorkflowEtapa.objects.get(ordem=1)
        except WorkflowEtapa.DoesNotExist:
            etapa_inicial = WorkflowEtapa.objects.first()

        WorkflowItem.objects.create(
            veiculo=veiculo,
            etapa_atual=etapa_inicial,
            tmv_prioridade=simulacao_tmv
        )
        
    def retrieve(self, request, *args, **kwargs):
        # Método padrão para GET (busca de um item específico)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        data = serializer.data
        try:
            avaliacao = AvaliacaoPreditiva.objects.get(veiculo=instance)
            data['avaliacao_preditiva'] = AvaliacaoPreditivaSerializer(avaliacao).data
        except AvaliacaoPreditiva.DoesNotExist:
            data['avaliacao_preditiva'] = None
            
        return Response(data)

    def create(self, request, *args, **kwargs):
        # CORREÇÃO FINAL: Sobrescreve o método POST para injetar a IA na resposta
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Pega a instância (veículo recém-criado)
        instance = serializer.instance 
        
        # Constrói a resposta final manualmente, incluindo o AvaliacaoPreditiva
        data = self.get_serializer(instance).data
        
        # Adiciona a avaliação preditiva (o retorno da IA)
        try:
            avaliacao = AvaliacaoPreditiva.objects.get(veiculo=instance)
            data['avaliacao_preditiva'] = AvaliacaoPreditivaSerializer(avaliacao).data
        except AvaliacaoPreditiva.DoesNotExist:
            data['avaliacao_preditiva'] = None

        return Response(data, status=status.HTTP_201_CREATED)