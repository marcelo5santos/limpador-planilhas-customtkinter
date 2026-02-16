from __future__ import annotations
import pandas as pd


def build_report(df_before: pd.DataFrame, df_after: pd.DataFrame, df_erros: pd.DataFrame, stats: dict) -> str:
    linhas_before = len(df_before)
    linhas_after = len(df_after)

    nulos_after = df_after.isna().sum().sort_values(ascending=False)
    dup_before = int(df_before.duplicated().sum())
    dup_after = int(df_after.duplicated().sum())

    erros_datas = int(stats.get("erros_datas", 0))
    erros_valores = int(stats.get("erros_valores", 0))
    total_erros = int(len(df_erros)) if df_erros is not None else 0

    linhas = []
    linhas.append("RELATÓRIO - LIMPEZA DE PLANILHA")
    linhas.append("")
    linhas.append(f"Linhas (antes): {linhas_before}")
    linhas.append(f"Linhas (depois): {linhas_after}")
    linhas.append("")
    linhas.append(f"Duplicadas (antes): {dup_before}")
    linhas.append(f"Duplicadas (depois): {dup_after}")
    linhas.append("")
    linhas.append(f"Erros de data (inválidas): {erros_datas}")
    linhas.append(f"Erros de valor (inválidos): {erros_valores}")
    linhas.append(f"Linhas com erros (aba ERROS): {total_erros}")
    linhas.append("")
    linhas.append("Nulos por coluna (depois):")
    linhas.extend([f"- {k}: {int(v)}" for k, v in nulos_after.items()])

    return "\n".join(linhas)
