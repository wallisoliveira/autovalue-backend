from rest_framework.routers import DefaultRouter
from .views import VeiculoViewSet, AvaliacaoPreditivaViewSet, WorkflowEtapaViewSet, WorkflowItemViewSet

# Usamos DefaultRouter para configurar rotas REST automaticamente
router = DefaultRouter()

# Rota principal para a gestão de veículos
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')

# Rotas para a gestão de avaliação (precificação)
router.register(r'avaliacoes', AvaliacaoPreditivaViewSet, basename='avaliacao')

# Rotas para o Kanban (etapas e itens)
router.register(r'workflow-etapas', WorkflowEtapaViewSet, basename='workflow-etapas')
router.register(r'workflow-itens', WorkflowItemViewSet, basename='workflow-itens')

urlpatterns = router.urls