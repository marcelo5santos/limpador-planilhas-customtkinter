from __future__ import annotations

import logging
import threading
import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from processor import process_file
from utils import default_output_paths


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Limpador de Planilhas (MVP)")
        self.geometry("780x420")

        self.input_path: str | None = None

        # UI
        self.header = ctk.CTkLabel(self, text="Limpador/Normalizador de Planilhas", font=ctk.CTkFont(size=22, weight="bold"))
        self.header.pack(pady=(18, 8))

        self.sub = ctk.CTkLabel(self, text="Selecione um CSV/XLSX, processe e gere Excel limpo + relatório.")
        self.sub.pack(pady=(0, 12))

        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=18, pady=10)

        self.path_label = ctk.CTkLabel(frame, text="Arquivo: (nenhum selecionado)")
        self.path_label.pack(anchor="w", padx=12, pady=(12, 6))

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=(0, 12))

        self.btn_pick = ctk.CTkButton(btns, text="Escolher arquivo", command=self.pick_file)
        self.btn_pick.pack(side="left")

        self.btn_run = ctk.CTkButton(btns, text="Processar", command=self.run, state="disabled")
        self.btn_run.pack(side="left", padx=10)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=18, pady=(18, 6))

        self.status = ctk.CTkLabel(self, text="Status: aguardando arquivo…")
        self.status.pack(anchor="w", padx=18)

        self.out_box = ctk.CTkTextbox(self, height=140)
        self.out_box.pack(fill="both", expand=True, padx=18, pady=14)
        self._log("Pronto. Selecione um arquivo CSV ou XLSX.\n")

    def _log(self, msg: str):
        self.out_box.insert("end", msg + "\n")
        self.out_box.see("end")

    def pick_file(self):
        path = fd.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Planilhas", "*.xlsx *.xls *.csv"), ("Todos", "*.*")]
        )
        if not path:
            return
        self.input_path = path
        self.path_label.configure(text=f"Arquivo: {path}")
        self.status.configure(text="Status: pronto para processar.")
        self.btn_run.configure(state="normal")
        self._log(f"Arquivo selecionado: {path}")

    def _set_busy(self, busy: bool):
        self.btn_pick.configure(state="disabled" if busy else "normal")
        self.btn_run.configure(state="disabled" if busy else ("normal" if self.input_path else "disabled"))

    def run(self):
        if not self.input_path:
            return

        self._set_busy(True)
        self.progress.set(0)
        self.status.configure(text="Status: iniciando…")
        self._log("Iniciando processamento…")

        in_path = self.input_path
        project_root = Path(__file__).resolve().parent.parent
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)

        base_name = Path(in_path).stem
        out_xlsx = str(output_dir / f"{base_name}_limpo.xlsx")
        out_report = str(output_dir / f"{base_name}_relatorio.txt")

        def progress_cb(value: float, message: str):
            # UI updates devem rodar no thread da UI:
            def _apply():
                self.progress.set(max(0.0, min(1.0, value)))
                self.status.configure(text=f"Status: {message}")
            self.after(0, _apply)

        def worker():
            try:
                result = process_file(
                    input_path=in_path,
                    out_xlsx=out_xlsx,
                    out_report=out_report,
                    progress=progress_cb,
                )
                def done_ok():
                    self._log("✅ Finalizado!")
                    self._log(f"Saída Excel: {result.out_xlsx}")
                    self._log(f"Relatório: {result.out_report}")
                    self._log(f"Linhas: {result.linhas_before} → {result.linhas_after}")
                    self._set_busy(False)
                self.after(0, done_ok)
            except Exception as e:
                logger.exception("Erro ao processar")
                def done_err():
                    self._log(f"❌ Erro: {e}")
                    self.status.configure(text="Status: erro ao processar.")
                    self._set_busy(False)
                self.after(0, done_err)

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
