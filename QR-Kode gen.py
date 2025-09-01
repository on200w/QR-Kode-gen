import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
import qrcode
import qrcode.image.svg


# -------------------------
# Funksjoner
# -------------------------
def generate_qr():
    """Generer QR-kode med eller uten logo."""
    url = entry_url.get().strip()
    if not url:
        messagebox.showerror("Feil", "Vennligst skriv inn en lenke.")
        return

    # Lag QR-kode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Viktig for logo
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=fg_color.get(),
        back_color=bg_color.get()
    ).convert("RGB")

    # Hvis logo er valgt, legg den til
    if logo_path.get():
        try:
            logo = Image.open(logo_path.get())
            logo_size = int(img.size[0] * 0.2)  # 20% av QR-bredden
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke legge til logo:\n{e}")

    # Forhåndsvisning
    preview_img = img.resize((200, 200))
    preview_tk = ImageTk.PhotoImage(preview_img)
    preview_label.config(image=preview_tk)
    preview_label.image = preview_tk

    # Lagre originalbilde for senere lagring
    global qr_image
    qr_image = img


def save_qr():
    """Lagre QR-kode i valgt format."""
    if qr_image is None:
        messagebox.showerror("Feil", "Generer en QR-kode først.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG-bilder", "*.png"),
            ("JPEG-bilder", "*.jpg"),
            ("SVG-filer", "*.svg")
        ],
        title="Lagre QR-kode som"
    )

    if filepath:
        try:
            if filepath.lower().endswith(".svg"):
                # Generer SVG separat
                factory = qrcode.image.svg.SvgImage
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                qr.add_data(entry_url.get().strip())
                qr.make(fit=True)
                img_svg = qr.make_image(image_factory=factory)
                with open(filepath, "wb") as f:
                    img_svg.save(f)
            elif filepath.lower().endswith(".jpg"):
                qr_image.convert("RGB").save(filepath, "JPEG")
            else:
                qr_image.save(filepath)
            messagebox.showinfo("Ferdig", f"QR-koden ble lagret til:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke lagre fil:\n{e}")


def choose_fg_color():
    """Velg forgrunnsfarge."""
    color = colorchooser.askcolor(title="Velg forgrunnsfarge")[1]
    if color:
        fg_color.set(color)


def choose_bg_color():
    """Velg bakgrunnsfarge."""
    color = colorchooser.askcolor(title="Velg bakgrunnsfarge")[1]
    if color:
        bg_color.set(color)


def choose_logo():
    """Velg logo-fil."""
    path = filedialog.askopenfilename(
        filetypes=[("Bilder", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if path:
        logo_path.set(path)


# -------------------------
# GUI-oppsett
# -------------------------
root = tk.Tk()
root.title("QR-kode Generator")
root.geometry("420x550")
root.resizable(False, False)

# Variabler
fg_color = tk.StringVar(value="black")
bg_color = tk.StringVar(value="white")
logo_path = tk.StringVar(value="")
qr_image = None

# Tittel
tk.Label(root, text="QR-kode Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Inputfelt
tk.Label(root, text="Skriv inn lenken:").pack()
entry_url = tk.Entry(root, width=45)
entry_url.pack(pady=5)

# Fargevalg
color_frame = tk.Frame(root)
color_frame.pack(pady=5)
tk.Button(color_frame, text="Velg forgrunnsfarge", command=choose_fg_color).grid(row=0, column=0, padx=5)
tk.Button(color_frame, text="Velg bakgrunnsfarge", command=choose_bg_color).grid(row=0, column=1, padx=5)

# Logo-knapp
tk.Button(root, text="Velg logo (valgfritt)", command=choose_logo).pack(pady=5)

# Knapper
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Generer QR-kode", command=generate_qr, width=18).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Lagre QR-kode", command=save_qr, width=18).grid(row=0, column=1, padx=5)

# Forhåndsvisning
preview_label = tk.Label(root, text="Forhåndsvisning vises her", width=200, height=200)
preview_label.pack(pady=10)

# Start GUI
root.mainloop()
