def normalizar_valor(valor):
    if valor is None:
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    if not isinstance(valor, str):
        return 0.0

    cleaned = (
        valor.replace("R$", "")
             .replace(" ", "")
             .replace(".", "")
             .replace(",", ".")
             .strip()
    )
    if not cleaned:
        return 0.0

    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def indexar_pagamentos(pagamentos):
    index = {}
    for p in pagamentos:
        venda_id = p.get("id_venda") or p.get("venda_id") or p.get("id")
        valor = normalizar_valor(p.get("valor"))
        if venda_id is None:
            continue
        index.setdefault(venda_id, []).append({"id_venda": venda_id, "valor": valor})
    return index

def reconciliar(vendas, pagamentos):
    """
    Reconcilia vendas com pagamentos.

    Retorna:
    pagos_corretos,
    pagos_com_diferenca,
    pendentes,
    pagamentos_sem_venda,
    duplicados
    """
    vendas_por_id = {}
    for v in vendas:
        venda_id = v.get("id")
        if venda_id is None:
            continue
        vendas_por_id[venda_id] = {
            "id": venda_id,
            "cliente": v.get("cliente"),
            "valor_venda": normalizar_valor(v.get("valor_venda") or v.get("valor")),
        }

    pagamentos_index = indexar_pagamentos(pagamentos)

    pagamentos_sem_venda = []
    for p in pagamentos:
        venda_id = p.get("id_venda") or p.get("venda_id") or p.get("id")
        if venda_id is None:
            continue
        if venda_id not in vendas_por_id:
            pagamentos_sem_venda.append({
                "id": venda_id,
                "valor": round(normalizar_valor(p.get("valor")), 2),
            })

    pagos_corretos = []
    pagos_com_diferenca = []
    pendentes = []
    duplicados = []

    for venda_id, venda in vendas_por_id.items():
        pagamentos_venda = pagamentos_index.get(venda_id, [])
        total_pago = round(sum(p["valor"] for p in pagamentos_venda), 2)
        valor_venda = round(venda["valor_venda"], 2)
        pendente = round(valor_venda - total_pago, 2)

        if len(pagamentos_venda) > 1:
            duplicados.append({"id": venda_id, "qtd": len(pagamentos_venda)})

        if pendente > 0:
            pendentes.append({
                "id": venda_id,
                "cliente": venda.get("cliente"),
                "valor_venda": valor_venda,
                "total_pago": total_pago,
                "pendente": pendente,
            })
            pagos_com_diferenca.append({"id": venda_id, "pendente": pendente})
        elif pendente == 0:
            pagos_corretos.append({"id": venda_id})
        else:
            pagos_com_diferenca.append({"id": venda_id, "pendente": pendente})

    return (
        pagos_corretos,
        pagos_com_diferenca,
        pendentes,
        pagamentos_sem_venda,
        duplicados,
    )
