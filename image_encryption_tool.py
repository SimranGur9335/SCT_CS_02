import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Function to encrypt/decrypt using XOR operation
def process_image(file_path, key, mode):
    try:
        img = Image.open(file_path)
        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                px = pixels[i, j]
                if len(px) == 4:
                    r, g, b, a = px
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key, a)
                else:
                    r, g, b = px
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key)

        output_path = f"output_images/{os.path.splitext(os.path.basename(file_path))[0]}_{mode}.png"
        img.save(output_path)
        messagebox.showinfo("Success", f"Image {mode}ed successfully!\nSaved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# File chooser
def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Trigger process
def trigger_process(mode):
    path = entry_file_path.get()
    try:
        key = int(entry_key.get())
        if not path or not os.path.exists(path):
            raise ValueError("Please choose a valid image file.")
        if not (0 <= key <= 255):
            raise ValueError("Key must be between 0 and 255.")
        process_image(path, key, mode)
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))

# GUI Setup
root = tk.Tk()
root.title("Image Encryption Tool")
root.geometry("400x250")
root.configure(bg="#1e1e1e")

# Styling function
def style_label(widget):
    widget.configure(bg="#1e1e1e", fg="white", font=("Segoe UI", 11))

# UI Elements
label1 = tk.Label(root, text="Choose an image file:")
style_label(label1)
label1.pack(pady=5)

entry_file_path = tk.Entry(root, width=40, bg="#333", fg="white", insertbackground="white")
entry_file_path.pack(pady=5)

tk.Button(root, text="Browse", command=choose_file, bg="#00bcd4", fg="#1e1e1e").pack(pady=5)

label2 = tk.Label(root, text="Enter encryption key (0-255):")
style_label(label2)
label2.pack(pady=5)

entry_key = tk.Entry(root, width=10, bg="#333", fg="white", insertbackground="white")
entry_key.pack(pady=5)

tk.Button(root, text="Encrypt Image", command=lambda: trigger_process("encrypt"), bg="#4caf50", fg="white").pack(pady=5)
tk.Button(root, text="Decrypt Image", command=lambda: trigger_process("decrypt"), bg="#f44336", fg="white").pack(pady=5)

root.mainloop()
