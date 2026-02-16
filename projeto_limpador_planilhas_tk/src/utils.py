import re
from pathlib import Path


def slugify_columns(cols: list[str]) -> list[str]:
    out = []
    for c in cols:
        c2 = str(c).strip().lower()
        c2 = re.sub(r"\s+", "_", c2)
        c2 = re.sub(r"[^a-z0-9_]", "", c2)
        c2 = re.sub(r"_+", "_", c2).strip("_")
        out.append(c2 if c2 else "col")
    return out


def default_output_paths(input_path: str) -> tuple[str, str]:
    p = Path(input_path)
    base = p.with_suffix("")
    out_xlsx = str(base.parent / f"{base.name}_limpo.xlsx")
    out_report = str(base.parent / f"{base.name}_relatorio.txt")
    return out_xlsx, out_report
