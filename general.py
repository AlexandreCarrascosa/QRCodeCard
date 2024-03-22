import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import qrcode
import vobject
import os

def generate_vcard_qr_code(name, phone_number, email, output_folder):
    phone = f"{phone_number}"

    # Criar o objeto vCard
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=name)
    vcard.add('fn')
    vcard.fn.value = name
    vcard.add('tel')
    vcard.tel.value = phone
    vcard.add('email')
    vcard.email.value = email

    # Converter vCard para string
    vcard_content = vcard.serialize()

    # Gerar QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_content)
    qr.make(fit=True)

    # Criar imagem do QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Salvar a imagem do QR code na pasta especificada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    qr_image.save(os.path.join(output_folder, f"vcard_qr_{name}.png"))

def process_excel_file(file_path):
    try:
        # Abrir o diálogo de seleção de pasta
        output_folder = filedialog.askdirectory(title="Selecionar pasta para salvar QR Codes")
        if not output_folder:
            messagebox.showinfo("Info", "Operação cancelada.")
            return
        
        # Ler o arquivo Excel
        df = pd.read_excel(file_path)
        
        # Verificar se as colunas necessárias estão presentes
        if not all(col in df.columns for col in ["Nome", "Telefone", "Email"]):
            raise ValueError("O arquivo Excel não possui as colunas necessárias.")
        
        # Criar QR codes para cada linha do DataFrame
        for index, row in df.iterrows():
            generate_vcard_qr_code(row["Nome"], row["Telefone"], row["Email"], output_folder)
        
        messagebox.showinfo("Sucesso", "QR Codes gerados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo Excel: {str(e)}")

def open_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")])
    if file_path:
        process_excel_file(file_path)

def generate_qr_code_from_form():
    name = name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    if not name or not phone_number or not email:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Abrir o diálogo de seleção de pasta
    output_folder = filedialog.askdirectory(title="Selecionar pasta para salvar QR Codes")
    if not output_folder:
        messagebox.showinfo("Info", "Operação cancelada.")
        return

    generate_vcard_qr_code(name, phone_number, email, output_folder)
    messagebox.showinfo("Sucesso", "QR Code gerado com sucesso!")

# Criar a janela
root = tk.Tk()
root.title("Gerador de QR Codes")
root.geometry("400x300")  # Definindo o tamanho da janela

# Criar guias (tabs)
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Importar Excel')
tab_control.add(tab2, text='Preencher Manualmente')
tab_control.pack(expand=1, fill='both')

# Tab 1: Importar Excel
load_button = tk.Button(tab1, text="Carregar Excel", font=("Arial", 12), command=open_excel_file)
load_button.pack(pady=20)

# Tab 2: Preencher Manualmente
name_label = tk.Label(tab2, text="Nome:", font=("Arial", 12))
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(tab2, font=("Arial", 9), width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = tk.Label(tab2, text="Telefone:", font=("Arial", 12))
phone_label.grid(row=1, column=0, padx=5, pady=5)
phone_number_entry = tk.Entry(tab2, font=("Arial", 9), width=40)
phone_number_entry.grid(row=1, column=1, pady=5)

email_label = tk.Label(tab2, text="Email:", font=("Arial", 12))
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(tab2, font=("Arial", 9), width=40)
email_entry.grid(row=2, column=1, padx=5, pady=5)

generate_button = tk.Button(tab2, text="Gerar QR Code", font=("Arial", 12), command=generate_qr_code_from_form)
generate_button.grid(row=3, columnspan=2, padx=10, pady=10)

root.mainloop()