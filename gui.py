import customtkinter as ctk
from tkinter import filedialog

class ImageStraightenerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Straightener Pro")
        self.geometry("1200x800")
        ctk.CTkButton(self, text="Open Image", command=self.open_image).pack(pady=20)
        self.label = ctk.CTkLabel(self, text="Project created successfully!")
        self.label.pack()

    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.jpeg *.png *.bmp *.tif *.tiff")])
        if filename:
            self.label.configure(text=filename)
