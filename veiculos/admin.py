from django.contrib import admin
from .models import Veiculo, AvaliacaoPreditiva, WorkflowEtapa, WorkflowItem, ModeloVeiculo # <-- Importe ModeloVeiculo

# 1. Registro para as Etapas do Kanban
@admin.register(WorkflowEtapa)
class WorkflowEtapaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')
    ordering = ('ordem',)

# 2. Registro do Veículo
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'status', 'data_entrada')
    list_filter = ('status', 'marca', 'ano')
    search_fields = ('placa', 'modelo')

# 3. Registro dos Itens de Avaliação e Workflow
admin.site.register(AvaliacaoPreditiva)
admin.site.register(WorkflowItem)

# 4. Registro do ModeloVeiculo para inserção manual
@admin.register(ModeloVeiculo) # <-- Adicione este bloco
class ModeloVeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'nome_modelo')
    list_filter = ('marca',)
    search_fields = ('nome_modelo',)

# ... (registros de AvaliacaoPreditiva e WorkflowItem) ...