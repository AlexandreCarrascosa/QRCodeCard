import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import qrcode
import vobject

def generate_card():
    # Obtém os valores dos campos
    name = name_entry.get()
    function = function_entry.get()
    department = department_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    # Verifica se todos os campos estão preenchidos
    if not all([name, function, department, phone, email, photo_path]):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos e selecione uma foto.")
        return

    # Cria o objeto vCard
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=name)
    vcard.add('fn')
    vcard.fn.value = name
    vcard.add('title')
    vcard.title.value = function
    vcard.add('org')
    vcard.org.value = department
    vcard.add('tel')
    vcard.tel.value = phone
    vcard.add('email')
    vcard.email.value = email

    # Converte vCard para string
    vcard_content = vcard.serialize()

    # Gera o QRCode com as informações do vCard
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_content)
    qr.make(fit=True)

    # Cria a imagem do QRCode
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Redimensiona o QRCode para caber no cartão
    qr_image = qr_image.resize((150, 150))

    # Abre a foto selecionada
    photo = Image.open(photo_path)
    photo = photo.resize((150, 150), Image.LANCZOS)

    # Cria um novo cartão com a foto, título, departamento e QRCode
    card = Image.new('RGB', (300, 450), color='white')
    draw = ImageDraw.Draw(card)

    # Posiciona a foto no topo
    card.paste(circular_image(photo), (75, 50), mask=circular_mask((150, 150)))

    # Adiciona o título e o departamento abaixo da foto
    function_width, function_height = draw.textsize(function)
    department_width, department_height = draw.textsize(department)

    function_position = (150 - function_width) / 2 + 75  # Centraliza horizontalmente
    department_position = (150 - department_width) / 2 + 75  # Centraliza horizontalmente

    draw.text((function_position, 230), f"{function}", fill="black")
    draw.text((department_position, 250), f"{department}", fill="black")

    # Adiciona o QRCode abaixo do título e departamento
    card.paste(qr_image, (75, 300))

    # Pergunta ao usuário onde deseja salvar o cartão
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    # Salva o cartão se o usuário selecionar um local
    if save_path:
        card.save(save_path)
        messagebox.showinfo("Sucesso", f"Cartão de contato gerado e salvo em:\n{save_path}")

        # Limpa os campos
        name_entry.delete(0, tk.END)
        function_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        photo_label.config(image=None)

def select_photo():
    global photo_path
    photo_path = filedialog.askopenfilename()
    if photo_path:
        photo = Image.open(photo_path)
        photo = photo.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(circular_image(photo))
        photo_label.config(image=photo)
        photo_label.image = photo

def circular_image(image):
    # Aplica uma máscara circular à imagem
    mask = circular_mask(image.size)
    result = Image.new("RGBA", image.size, 0)
    result.paste(image, (0, 0), mask)
    return result

def circular_mask(size):
    # Cria uma máscara circular
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask

root = tk.Tk()
root.title("Gerador de Cartão de Contato")
root.geometry("400x550")

# Nome
name_label = tk.Label(root, text="Nome:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Função
function_label = tk.Label(root, text="Função:")
function_label.pack()
function_entry = tk.Entry(root)
function_entry.pack()

# Departamento
department_label = tk.Label(root, text="Departamento:")
department_label.pack()
department_entry = tk.Entry(root)
department_entry.pack()

# Telefone
phone_label = tk.Label(root, text="Telefone:")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

# E-mail
email_label = tk.Label(root, text="E-mail:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

# Botão para selecionar foto
select_photo_button = tk.Button(root, text="Selecionar Foto", command=select_photo)
select_photo_button.pack()

# Label para exibir a foto selecionada
photo_label = tk.Label(root)
photo_label.pack()

# Botão para gerar cartão de contato
generate_button = tk.Button(root, text="Gerar Cartão de Contato", command=generate_card)
generate_button.pack()

root.mainloop()
