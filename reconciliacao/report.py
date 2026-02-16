from .core import reconciliar, normalizar_valor

def gerar_report(vendas, pagamentos):
    """
    Retorna:
    {
        "kpis": {
    "total_vendas": float,
    "total_recebido": float,
    "total_pendente": float,
    "qtd_pendentes": int,
    "qtd_pagamentos_sem_venda": int,
    "qtd_vendas_com_duplicidade": int,
}
,
        "top_pendencias": [...],
        "alertas": [...]
    }
    """
    (
        pagos_corretos,
        pagos_com_diferenca,
        pendentes,
        pagamentos_sem_venda,
        duplicados,
    ) = reconciliar(vendas, pagamentos)

    total_vendas = round(sum(normalizar_valor(v.get("valor_venda") or v.get("valor")) for v in vendas), 2)
    total_recebido = round(sum(normalizar_valor(p.get("valor")) for p in pagamentos), 2)
    total_pendente = round(sum(p["pendente"] for p in pendentes), 2)

    kpis = {
        "total_vendas": total_vendas,
        "total_recebido": total_recebido,
        "total_pendente": total_pendente,
        "qtd_pendentes": len(pendentes),
        "qtd_pagamentos_sem_venda": len(pagamentos_sem_venda),
        "qtd_vendas_com_duplicidade": len(duplicados),
    }

    top_pendencias = sorted(pendentes, key=lambda x: x["pendente"], reverse=True)

    alertas = []
    if kpis["qtd_pendentes"] > 0:
        alertas.append(
            f"ALERTA: {kpis['qtd_pendentes']} vendas pendentes (R$ {format_brl(total_pendente)})"
        )

    for p in pagamentos_sem_venda:
        alertas.append(
            f"ALERTA: Pagamento sem venda encontrado: {p['id']} (R$ {format_brl(p['valor'])})"
        )

    for d in duplicados:
        alertas.append(
            f"ALERTA: Venda {d['id']} com pagamento duplicado ({d['qtd']} lançamentos)"
        )

    return {
        "kpis": kpis,
        "top_pendencias": top_pendencias,
        "alertas": alertas,
    }

def format_brl(valor):
    return f"{round(valor, 2):.2f}".replace(".", ",")

