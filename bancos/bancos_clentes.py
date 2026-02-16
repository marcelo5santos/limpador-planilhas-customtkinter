vendas = [
    {"id": "V001", "cliente": "Ana", "valor": 199.90},
    {"id": "V002", "cliente": "Bruno", "valor": 149.90},
    {"id": "V003", "cliente": "Carla", "valor": 79.90},
    {"id": "V004", "cliente": "Diego", "valor": 299.90},
    {"id": "V005", "cliente": "Eva", "valor": 199.90},
]

pagamentos = [
    {"ref": "V001", "valor": 199.90},
    {"ref": "V002", "valor": 150.00},   # pago a mais
    {"ref": "V002", "valor": 150.00},   # duplicado
    {"ref": "V004", "valor": 299.90},
    {"ref": "V999", "valor": 50.00},    # pagamento sem venda
]


def indexar_pagamentos(pagamentos):
    """retorna dict: ref -> lista de valores pagos"""
    pagamentos_dict = {}
    for pagamento in pagamentos:
        ref = pagamento["ref"]
        pagamentos_dict.setdefault(ref, []).append(pagamento["valor"])
    return pagamentos_dict


def normalizar_valor(valor):
    return round(valor, 2)


def montar_diferenca(venda_id, valor_venda, valores_pagos):
    total_pago = sum(valores_pagos)
    return {
        "id": venda_id,
        "valor_venda": normalizar_valor(valor_venda),
        "valores_pagos": valores_pagos,
        "diferenca_total": normalizar_valor(total_pago - valor_venda),
    }


def reconciliar(vendas, pagamentos):
    """
    retorna:
    pagos_corretos,
    pagos_com_diferenca,
    pendentes,
    pagamentos_sem_venda,
    duplicados
    """
    vendas_dict = {venda["id"]: venda for venda in vendas}
    pagamentos_dict = indexar_pagamentos(pagamentos)

    pagos_corretos = []
    pagos_com_diferenca = []
    pendentes = []
    pagamentos_sem_venda = []
    duplicados = []

    for venda_id, venda in vendas_dict.items():
        valor_venda = venda["valor"]
        valores_pagos = pagamentos_dict.get(venda_id, [])

        if not valores_pagos:
            pendentes.append(venda.copy())
            continue

        total_pago = normalizar_valor(sum(valores_pagos))
        valor_venda_norm = normalizar_valor(valor_venda)
        pagamento_unico = len(valores_pagos) == 1
        valor_exato = total_pago == valor_venda_norm

        if len(valores_pagos) > 1:
            duplicados.append(venda.copy())

        if pagamento_unico and valor_exato:
            pagos_corretos.append(venda.copy())
        else:
            pagos_com_diferenca.append(montar_diferenca(venda_id, valor_venda, valores_pagos))

    for ref, valores_pagos in pagamentos_dict.items():
        if ref not in vendas_dict:
            for valor in valores_pagos:
                pagamentos_sem_venda.append({"ref": ref, "valor": valor})

    return (
        pagos_corretos,
        pagos_com_diferenca,
        pendentes,
        pagamentos_sem_venda,
        duplicados,
    )


(
    pagos_corretos,
    pagos_com_diferenca,
    pendentes,
    pagamentos_sem_venda,
    duplicados,
) = reconciliar(vendas, pagamentos)

print("pagos_corretos:", pagos_corretos)
print("pagos_com_diferenca:", pagos_com_diferenca)
print("pendentes:", pendentes)
print("pagamentos_sem_venda:", pagamentos_sem_venda)
print("duplicados:", duplicados)
