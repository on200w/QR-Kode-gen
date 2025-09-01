import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
import qrcode

def generate_qr():
    url = entry.get().strip()
    if not url:
        messagebox.showerror("Feil", "Vennligst skriv inn en lenke.")
        return

    # Lag QR-koden
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color.get(), back_color=bg_color.get())
    preview_img = img.resize((200, 200))
    preview_tk = ImageTk.PhotoImage(preview_img)

    preview_label.config(image=preview_tk)
    preview_label.image = preview_tk
    global qr_image
    qr_image = img  # lagre for senere lagring

def save_qr():
    if qr_image is None:
        messagebox.showerror("Feil", "Generer en QR-kode først.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG-bilder", "*.png")],
        title="Lagre QR-kode som"
    )
    if filepath:
        qr_image.save(filepath)
        messagebox.showinfo("Ferdig", f"QR-koden ble lagret til:\n{filepath}")

def choose_fg_color():
    color = colorchooser.askcolor(title="Velg forgrunnsfarge")[1]
    if color:
        fg_color.set(color)

def choose_bg_color():
    color = colorchooser.askcolor(title="Velg bakgrunnsfarge")[1]
    if color:
        bg_color.set(color)

# Opprett GUI
root = tk.Tk()
root.title("QR-kode Generator")
root.geometry("400x500")
root.resizable(False, False)

fg_color = tk.StringVar(value="black")
bg_color = tk.StringVar(value="white")
qr_image = None

# Tittel
tk.Label(root, text="QR-kode Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Inputfelt
tk.Label(root, text="Skriv inn lenken:").pack()
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Fargevalg
color_frame = tk.Frame(root)
color_frame.pack(pady=5)
tk.Button(color_frame, text="Velg forgrunnsfarge", command=choose_fg_color).grid(row=0, column=0, padx=5)
tk.Button(color_frame, text="Velg bakgrunnsfarge", command=choose_bg_color).grid(row=0, column=1, padx=5)

# Knapper
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Generer QR-kode", command=generate_qr, width=18).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Lagre QR-kode", command=save_qr, width=18).grid(row=0, column=1, padx=5)

# Forhåndsvisning
preview_label = tk.Label(root, text="Forhåndsvisning vises her", width=200, height=200)
preview_label.pack(pady=10)

root.mainloop()