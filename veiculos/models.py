# Em veiculos/models.py (CÓDIGO CORRIGIDO)

from django.db import models
from django.contrib.auth.models import User  # Importamos User para ligar ao avaliador

# --- 1. Modelo Veiculo ---
class Veiculo(models.Model):
    # Identificação
    placa = models.CharField(max_length=7, unique=True, verbose_name="Placa do Veículo")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField(verbose_name="Ano Fabricação")
    quilometragem = models.IntegerField()
    cor = models.CharField(max_length=30)
    
    # Estado de Negócio
    status = models.CharField(
        max_length=20,
        choices=[
            ('AVALIACAO', 'Em Avaliação'),
            ('COMPRADO', 'Comprado - Em Preparação'),
            ('ESTOQUE', 'Em Estoque - Pronto para Venda'),
            ('VENDIDO', 'Vendido')
        ],
        default='AVALIACAO'
    )
    
    # CAMPOS DE DATA QUE ESTAVAM FALTANDO OU DESALINHADOS NA CLASSE VEICULO
    data_entrada = models.DateTimeField(auto_now_add=True, verbose_name="Data de Entrada na Avaliação")
    data_compra = models.DateTimeField(null=True, blank=True, verbose_name="Data da Compra Efetiva")
    data_venda = models.DateTimeField(null=True, blank=True, verbose_name="Data da Venda")
    
    # Preços
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço Pago")
    preco_anuncio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço Anunciado")

    # Referência
    avaliador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Avaliador/Comprador")

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.placa}"


# --- 2. Modelo de Dados Auxiliar (Nível superior) ---
class ModeloVeiculo(models.Model):
    # O campo 'marca' será usado como chave de agrupamento
    marca = models.CharField(max_length=50) 
    nome_modelo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.marca} - {self.nome_modelo}"
    
    class Meta:
        # Garante que não há modelos duplicados para a mesma marca
        unique_together = ('marca', 'nome_modelo')


# --- 3. Modelo AvaliacaoPreditiva ---
class AvaliacaoPreditiva(models.Model):
    # Chave ligada ao Veículo (relacionamento 1 para 1)
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, primary_key=True)
    
    # Dados da IA (Outputs em BRANCO)
    preco_maximo_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PMC Sugerido pela IA")
    tmv_previsto_dias = models.IntegerField(verbose_name="TMV Previsto (dias)")
    margem_desejada = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Margem Desejada (%)") 
    
    # Preços de Mercado para comparação (via Data Scraping)
    fipe_referencia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Tabela FIPE")
    mercado_medio_concorrencia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Médio Concorrência")
    
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.veiculo.placa} ({self.data_avaliacao.strftime('%Y-%m-%d')})"


# --- 4. Modelos de Workflow/Logística ---
class WorkflowEtapa(models.Model):
    # Ex: 'Comprado', 'Detalhamento', 'Fotos/Anúncio', etc.
    nome = models.CharField(max_length=50, unique=True)
    ordem = models.IntegerField(unique=True, verbose_name="Ordem no Kanban")

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['ordem']


class WorkflowItem(models.Model):
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE)
    etapa_atual = models.ForeignKey(WorkflowEtapa, on_delete=models.PROTECT)
    
    # O item mais importante para priorização, puxado da AvaliacaoPreditiva
    tmv_prioridade = models.IntegerField(verbose_name="Prioridade (Baseada no TMV)") 
    
    data_inicio_etapa = models.DateTimeField(auto_now=True)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Workflow de {self.veiculo.placa} - Etapa: {self.etapa_atual.nome}"