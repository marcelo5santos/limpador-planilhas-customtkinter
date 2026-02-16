# Limpador/Normalizador de Planilhas (CustomTkinter)

Aplicativo desktop em Python para **padronizar planilhas CSV/XLSX** e gerar:
- Excel limpo (aba `DADOS`)
- Aba `ERROS` com registros inválidos (ex: data/valor inválidos)
- Relatório `.txt` com resumo do processamento

## Funcionalidades
- Padroniza nomes de colunas (snake_case)
- Padroniza dados:
  - `nome` → Title Case
  - `email` → lowercase
  - `data_de_pagamento` → dd/mm/aaaa (inválidas vão para `ERROS`, ausentes viram "Não informado")
  - `valor_r` → número com formatação de moeda (R$)
  - `observao` vazio → "Não informado"
- Remove duplicados
- Exporta `*_limpo.xlsx` e `*_relatorio.txt`

## Como executar (Windows)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
