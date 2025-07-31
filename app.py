import fitz  # PyMuPDF
import os
from math import ceil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

def split_pdf_into_strips(pdf_path, max_width_mm, max_height_mm, destination_folder, save_to_single_file, split_horizontally):
    try:
        doc = fitz.open(pdf_path)
        max_width_pt = (max_width_mm / 25.4) * 72
        max_height_pt = (max_height_mm / 25.4) * 72 if split_horizontally else None
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        if save_to_single_file:
            merged_pdf = fitz.open()

        for page_num, page in enumerate(doc):
            total_width = page.rect.width
            total_height = page.rect.height
            num_vertical = ceil(total_width / max_width_pt)
            num_horizontal = ceil(total_height / max_height_pt) if split_horizontally else 1

            for i in range(num_vertical):
                x0 = i * max_width_pt
                x1 = min((i + 1) * max_width_pt, total_width)

                for j in range(num_horizontal):
                    y0 = j * max_height_pt if split_horizontally else 0
                    y1 = min((j + 1) * max_height_pt, total_height) if split_horizontally else total_height

                    strip_rect = fitz.Rect(x0, y0, x1, y1)

                    new_page_pdf = fitz.open()
                    new_page = new_page_pdf.new_page(width=strip_rect.width, height=strip_rect.height)
                    new_page.show_pdf_page(new_page.rect, doc, page_num, clip=strip_rect)

                    if save_to_single_file:
                        merged_pdf.insert_pdf(new_page_pdf)
                    else:
                        suffix = f"_pagina{page_num+1}_coluna{i+1}"
                        if split_horizontally:
                            suffix += f"_linha{j+1}"
                        output_name = f"{base_name}{suffix}.pdf"
                        output_path = os.path.join(destination_folder, output_name)
                        new_page_pdf.save(output_path)

                    new_page_pdf.close()

        doc.close()

        if save_to_single_file:
            final_path = os.path.join(destination_folder, f"{base_name}_fatiado.pdf")
            merged_pdf.save(final_path)
            merged_pdf.close()
            messagebox.showinfo("Sucesso", f"PDF final salvo em:\n{final_path}")
        else:
            messagebox.showinfo("Sucesso", f"Arquivos salvos em:\n{destination_folder}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

def choose_pdf():
    path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if path:
        input_pdf.set(path)

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder.set(folder)

def run_split():
    pdf = input_pdf.get()
    folder = output_folder.get()
    width_str = max_width.get()
    height_str = max_height.get()

    if not pdf or not os.path.isfile(pdf):
        messagebox.showerror("Erro", "Selecione um arquivo PDF válido.")
        return
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Erro", "Selecione uma pasta de destino válida.")
        return
    try:
        width_mm = float(width_str.replace(",", "."))
        if width_mm <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Insira uma largura válida em milímetros.")
        return

    if split_horizontal.get():
        try:
            height_mm = float(height_str.replace(",", "."))
            if height_mm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Insira uma altura válida em milímetros.")
            return
    else:
        height_mm = 0

    split_pdf_into_strips(
        pdf_path=pdf,
        max_width_mm=width_mm,
        max_height_mm=height_mm,
        destination_folder=folder,
        save_to_single_file=save_single.get(),
        split_horizontally=split_horizontal.get()
    )

# Janela principal com tema escuro
window = ttk.Window(themename="cyborg")
window.title("PDF-slicer")
window.geometry("520x460")
window.resizable(False, False)

# Variáveis de estado
input_pdf = ttk.StringVar()
output_folder = ttk.StringVar()
max_width = ttk.StringVar(value="910")
max_height = ttk.StringVar(value="Sem limite.")
save_single = ttk.BooleanVar(value=True)
split_horizontal = ttk.BooleanVar(value=False)

# Layout
frame = ttk.Frame(window, padding=20)
frame.pack(fill=BOTH, expand=True)

ttk.Label(frame, text="PDF de entrada:").pack(anchor=W)
pdf_line = ttk.Frame(frame)
pdf_line.pack(fill=X, pady=4)
ttk.Entry(pdf_line, textvariable=input_pdf, width=50).pack(side=LEFT, fill=X, expand=True)
ttk.Button(pdf_line, text="Escolher PDF", command=choose_pdf, bootstyle=PRIMARY).pack(side=LEFT, padx=(5, 0))

ttk.Label(frame, text="Largura máxima da folha (mm):").pack(anchor=W, pady=(10, 0))
width_line = ttk.Frame(frame)
width_line.pack(fill=X, pady=4)
ttk.Entry(width_line, textvariable=max_width, width=50).pack(side=LEFT, fill=X, expand=True)

ttk.Label(frame, text="Pasta de destino:").pack(anchor=W, pady=(10, 0))
folder_line = ttk.Frame(frame)
folder_line.pack(fill=X, pady=4)
ttk.Entry(folder_line, textvariable=output_folder, width=50).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
ttk.Button(folder_line, text="Escolher Pasta", command=choose_folder, bootstyle=PRIMARY).pack(side=LEFT)

ttk.Checkbutton(
    frame,
    text="Cortar também na horizontal",
    variable=split_horizontal,
    bootstyle="info-round-toggle"
).pack(pady=(8, 0))

ttk.Label(frame, text="Altura máxima da folha (mm):").pack(anchor=W, pady=(10, 0))
h_line = ttk.Frame(frame)
h_line.pack(fill=X, pady=4)
# Entry para altura máxima, desabilitado se split_horizontal for False
height_entry = ttk.Entry(h_line, textvariable=max_height, width=10)
height_entry.pack(side=LEFT, fill=X, expand=True)

def update_height_state(*args):
    if split_horizontal.get():
        height_entry.config(state="normal")
        if max_height.get() == "Sem limite.":
            max_height.set("297")
    else:
        height_entry.config(state="disabled")
        max_height.set("Sem limite.")

split_horizontal.trace_add("write", update_height_state)
update_height_state()

ttk.Checkbutton(
    frame,
    text="Salvar todas as faixas em um único PDF",
    variable=save_single,
    bootstyle="success-round-toggle"
).pack(pady=8)


ttk.Button(frame, text="Cortar PDF", command=run_split, width=25, bootstyle="success").pack(pady=15)

window.mainloop()
