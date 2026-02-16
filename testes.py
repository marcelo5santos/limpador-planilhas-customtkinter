from datetime import datetime
raw_rows = [
    {"data": "2026-01-02", "cliente": " Ana  ", "produto": "Teclado", "valor": "R$ 199,90", "status": "Pago"},
    {"data": "02/01/2026", "cliente": "Bruno", "produto": "Mouse", "valor": "149.9", "status": "pago"},
    {"data": "2026/01/03", "cliente": "ana", "produto": "Monitor", "valor": "1.299,00", "status": "PENDENTE"},
    {"data": "03-01-2026", "cliente": "Carla", "produto": "Mouse", "valor": "R$ -20,00", "status": "ESTORNO"},
    {"data": "2026-01-04", "cliente": "  ", "produto": "Cabo HDMI", "valor": "39,90", "status": "Pago"},
    {"data": "2026-01-04", "cliente": "Diego", "produto": "", "valor": "R$ 79,90", "status": "Pago"},
    {"data": "2026-01-05", "cliente": "Eva", "produto": "Teclado", "valor": None, "status": "Pago"},
    {"data": None, "cliente": "Felipe", "produto": "Mouse", "valor": "R$ 89,90", "status": "Pago"},
]


DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y")
VALID_STATUS = {"PAGO", "PENDENTE", "ESTORNO", "OUTRO"}

def parse_date(value):
    if not value or not isinstance(value, str):
        return None
    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")  # ISO
        except ValueError:
            continue
    return None

def parse_money(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None

    cleaned = (
        value.replace("R$", "")
             .replace(" ", "")
             .replace(".", "")
             .replace(",", ".")
             .strip()
    )
    if not cleaned:
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None

def normalize_text(value, *, title=False):
    if not isinstance(value, str):
        return None
    text = " ".join(value.strip().split())  # remove espaços duplicados
    if not text:
        return None
    return text.title() if title else text

def normalize_status(value):
    if not value or not isinstance(value, str):
        return "OUTRO"
    text = value.strip().upper()
    if text in {"PAGO", "PENDENTE", "ESTORNO"}:
        return text
    return "OUTRO"

def clean_row(row):
    motivos = []

    data = parse_date(row.get("data"))
    if not data:
        motivos.append("data_invalida")

    cliente = normalize_text(row.get("cliente"), title=True)
    if not cliente:
        motivos.append("cliente_vazio")

    produto = normalize_text(row.get("produto"))
    if not produto:
        motivos.append("produto_vazio")

    valor = parse_money(row.get("valor"))
    if valor is None:
        motivos.append("valor_ausente_ou_invalido")
    elif valor <= 0:
        motivos.append("valor_nao_positivo")

    status = normalize_status(row.get("status"))
    if status not in VALID_STATUS:
        motivos.append("status_invalido")  # aqui é redundante, mas fica claro

    if motivos:
        return None, motivos

    return {
        "data": data,
        "cliente": cliente,
        "produto": produto,
        "valor": valor,
        "status": status,
    }, []

def process(rows):
    clean_rows = []
    rejected_rows = []

    for row in rows:
        clean, motivos = clean_row(row)
        if clean:
            clean_rows.append(clean)
        else:
            rejected_rows.append({"row": row, "motivos": motivos})

    pagos = [r for r in clean_rows if r["status"] == "PAGO"]
    receita_total = sum(r["valor"] for r in pagos)
    ticket_medio_pago = (receita_total / len(pagos)) if pagos else 0.0

    por_produto_pago = {}
    por_cliente_pago = {}

    for r in pagos:
        por_produto_pago[r["produto"]] = por_produto_pago.get(r["produto"], 0.0) + r["valor"]
        por_cliente_pago[r["cliente"]] = por_cliente_pago.get(r["cliente"], 0.0) + r["valor"]

    summary = {
        "total_linhas": len(rows),
        "aprovadas": len(clean_rows),
        "rejeitadas": len(rejected_rows),
        "receita_total": receita_total,
        "ticket_medio_pago": ticket_medio_pago,
        "por_produto_pago": por_produto_pago,
        "por_cliente_pago": por_cliente_pago,
    }
    return clean_rows, rejected_rows, summary

print(process(raw_rows))