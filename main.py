import tkinter as tk
from tkinter import messagebox, filedialog

from PIL import ImageTk

import qrcode
import vobject

def generate_qr_preview():
    name = name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    if not name or not phone_number or not email:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

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

    # Redimensionar a imagem do QR code para torná-la menor
    qr_image = qr_image.resize((100, 100))

    # Exibir imagem do QR code na área de visualização
    qr_img = ImageTk.PhotoImage(image=qr_image)
    qr_preview_label.config(image=qr_img)
    qr_preview_label.image = qr_img

def generate_vcard_qr_code():
    name = name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    if not name or not phone_number or not email:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    phone = f"{phone_number}"

    # Criar o objeto vCard
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=name)
    vcard.add('fn')
    vcard.fn.value = name
    vcard.add('tel')
    vcard.tel.value = phone

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

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        # Salvar a imagem do QR code
        qr_image.save(file_path)
        messagebox.showinfo("Sucesso", f"QR Code gerado e salvo em:\n{file_path}")

        # Limpar os campos
        name_entry.delete(0, tk.END)
        phone_number_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

# Criar a janela
root = tk.Tk()
root.title("Gerador de QR Code")
root.geometry("550x175")  # Definindo o tamanho da janela

# Nome
name_label = tk.Label(root, text="Nome:", font=("Arial", 12), anchor="w")
name_label.grid(row=0, column=0, padx=5, pady=5)

name_entry = tk.Entry(root, font=("Arial", 9), width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Telefone
phone_label = tk.Label(root, text="Telefone:", font=("Arial", 12), anchor="w")
phone_label.grid(row=1, column=0, padx=5, pady=5)

phone_number_entry = tk.Entry(root, font=("Arial", 9), width=40)
phone_number_entry.grid(row=1, column=1, padx=5 ,pady=5, sticky="w")

# Email
email_label = tk.Label(root, text="Email:", font=("Arial", 12), anchor="w")
email_label.grid(row=2, column=0, padx=5, pady=5)

email_entry = tk.Entry(root, font=("Arial", 9), width=40)
email_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

# Botão para gerar pré-visualização do QR Code
preview_button = tk.Button(root, text="Pré-visualizar QR Code", font=("Arial", 9), command=generate_qr_preview)
preview_button.grid(row=3, columnspan=2, padx=10, pady=10)

# Área de visualização do QR code
qr_preview_label = tk.Label(root, text="QR Code Preview", font=("Arial", 12))
qr_preview_label.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

# Botão para gerar QR Code
generate_button = tk.Button(root, text="Gerar QR Code", font=("Arial", 9), command=generate_vcard_qr_code)
generate_button.grid(row=3, column=2, padx=10, pady=10)

root.mainloop()
