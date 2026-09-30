import os
import tkinter as tk
from PIL import Image, ImageTk
import itertools

folder = 'img'
image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_cycle = itertools.cycle(image_files)

root = tk.Tk()
root.title("Image Slideshow")
root.attributes('-fullscreen', True)
root.overrideredirect(True)
root.configure(bg="black")

label = tk.Label(root, bg="black")
label.pack(expand=True, fill=tk.BOTH)

current_image_pil = None
photo = None

info_label = tk.Label(
    root,
    text="Press ESC to exit",
    font=('Segoe UI', 20),
    fg="white",
    bg="black"
)

info_label.place(relx=0.5, rely=0.95, anchor="center")
info_label.lift()

def hide_info_label():
    info_label.place_forget()

root.after(3000, hide_info_label)

def fit_image_to_window(image, window_size):
    image_width, image_height = image.size
    window_width, window_height = window_size

    if window_width <= 1 or window_height <= 1:
        return image

    aspect_ratio = image_width / image_height

    if (window_width / window_height) > aspect_ratio:
        new_height = window_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = window_width
        new_height = int(new_width / aspect_ratio)

    new_width = max(1, new_width)
    new_height = max(1, new_height)

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def update_image():
    global current_image_pil, photo

    root.update_idletasks()

    image_file = next(image_cycle)
    current_image_pil = Image.open(os.path.join(folder, image_file))

    w = max(1, root.winfo_width())
    h = max(1, root.winfo_height())

    resized = fit_image_to_window(current_image_pil, (w, h))

    photo = ImageTk.PhotoImage(resized)
    label.config(image=photo)
    label.image = photo

    info_label.lift()

    root.after(3000, update_image)

def resize_image(event):
    global photo
    if current_image_pil and event.widget == root:
        w = max(1, event.width)
        h = max(1, event.height)
        resized = fit_image_to_window(current_image_pil, (w, h))
        photo = ImageTk.PhotoImage(resized)
        label.config(image=photo)
        label.image = photo
        info_label.lift()

def exit_fullscreen(event=None):
    root.destroy()

root.bind("<Configure>", resize_image)
root.bind("<Escape>", exit_fullscreen)

update_image()
root.mainloop()