# veiculos/init_data.py
from veiculos.models import WorkflowEtapa

ETAPAS = [
    (1, 'Comprado / Em Avaliação Final'),
    (2, 'Preparação (Mecânica e Estética)'),
    (3, 'Fotos e Anúncio'),
    (4, 'Em Estoque / Pronto para Venda'),
    (5, 'Vendido'),
]

def create_initial_workflow_etapas():
    for ordem, nome in ETAPAS:
        WorkflowEtapa.objects.get_or_create(
            ordem=ordem,
            defaults={'nome': nome}
        )
    print("Etapas iniciais do Workflow criadas/verificadas com sucesso.")

if __name__ == '__main__':
    create_initial_workflow_etapas()