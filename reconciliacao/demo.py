try:
    from reconciliacao.core import reconciliar
    from reconciliacao.report import gerar_report
except ModuleNotFoundError:
    from core import reconciliar
    from report import gerar_report

vendas = [
    {"id": "V001", "cliente": "Ana", "valor_venda": 199.90},
    {"id": "V002", "cliente": "Bruno", "valor_venda": 149.90},
    {"id": "V003", "cliente": "Carla", "valor_venda": 79.90},
]

pagamentos = [
    {"id_venda": "V001", "valor": 199.90},
    {"id_venda": "V002", "valor": 100.00},
    {"id_venda": "V002", "valor": 49.90},
    {"id_venda": "V999", "valor": 50.00},
]

report = gerar_report(vendas, pagamentos)
print(report)
