import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import sys
import io
import img2pdf

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ImgToPdfApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image to PDF Converter - Modern")
        self.geometry("850x650")
        self.minsize(750, 550)
        
        # Set window icon
        icon_path = resource_path(os.path.join("resources", "icon.ico"))
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # state
        self.image_items = [] # list of dicts

        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # push convert button down

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Img2PDF", font=ctk.CTkFont(size=28, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_add = ctk.CTkButton(self.sidebar_frame, text="➕ Add Images", command=self.add_images, height=45, font=ctk.CTkFont(size=14))
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)

        self.btn_clear = ctk.CTkButton(self.sidebar_frame, text="🗑️ Clear All", command=self.clear_all, height=45, font=ctk.CTkFont(size=14), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_clear.grid(row=2, column=0, padx=20, pady=10)

        # Quality options
        self.quality_label = ctk.CTkLabel(self.sidebar_frame, text="PDF Quality:", anchor="w", font=ctk.CTkFont(size=14))
        self.quality_label.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.quality_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Low", "Medium", "High", "Lossless"], height=35)
        self.quality_optionmenu.grid(row=4, column=0, padx=20, pady=(5, 10))
        self.quality_optionmenu.set("High") # Default setting

        self.btn_convert = ctk.CTkButton(self.sidebar_frame, text="📄 Convert to PDF", command=self.convert_to_pdf, height=50, font=ctk.CTkFont(size=15, weight="bold"))
        self.btn_convert.grid(row=5, column=0, padx=20, pady=30)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("System")

        # --- Main Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(self.main_frame, text="Selected Images", font=ctk.CTkFont(size=22, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=25, pady=(20, 15), sticky="w")

        # Scrollable Frame for Images
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10, fg_color=("gray95", "gray13"))
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def add_images(self):
        filepaths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
                ("All Files", "*.*")
            ]
        )
        for filepath in filepaths:
            # check if already added
            if not any(item['path'] == filepath for item in self.image_items):
                self.create_image_item(filepath)
                
    def create_image_item(self, filepath):
        # Create thumbnail
        try:
            img = Image.open(filepath)
            # Create a square thumbnail
            img.thumbnail((70, 70))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(70, 70))
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return
            
        index = len(self.image_items)
        
        # Item frame
        item_frame = ctk.CTkFrame(self.scrollable_frame, height=90, corner_radius=10, fg_color=("white", "gray20"))
        item_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=8)
        item_frame.grid_columnconfigure(2, weight=1) # push buttons to right
        item_frame.grid_propagate(False) # keep height fixed

        # Image label
        img_label = ctk.CTkLabel(item_frame, image=ctk_img, text="", corner_radius=5)
        img_label.grid(row=0, column=0, padx=15, pady=10)

        # Filename label
        filename = os.path.basename(filepath)
        name_label = ctk.CTkLabel(item_frame, text=filename, font=ctk.CTkFont(size=15))
        name_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Buttons frame (Up, Down, Remove)
        action_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        action_frame.grid(row=0, column=2, padx=15, pady=10, sticky="e")

        btn_up = ctk.CTkButton(action_frame, text="▲", width=36, height=36, font=ctk.CTkFont(size=14), command=lambda p=filepath: self.move_item(p, -1))
        btn_up.pack(side="left", padx=4)

        btn_down = ctk.CTkButton(action_frame, text="▼", width=36, height=36, font=ctk.CTkFont(size=14), command=lambda p=filepath: self.move_item(p, 1))
        btn_down.pack(side="left", padx=4)

        btn_remove = ctk.CTkButton(action_frame, text="✕", width=36, height=36, font=ctk.CTkFont(size=14), fg_color="#E74C3C", hover_color="#C0392B", command=lambda p=filepath: self.remove_item(p))
        btn_remove.pack(side="left", padx=(15, 0))

        item_dict = {
            'path': filepath,
            'frame': item_frame,
            'image': ctk_img, # keep reference to prevent garbage collection
            'btn_up': btn_up,
            'btn_down': btn_down,
            'btn_remove': btn_remove
        }
        self.image_items.append(item_dict)
        self.refresh_ui_order()

    def move_item(self, filepath, direction):
        idx = next((i for i, item in enumerate(self.image_items) if item['path'] == filepath), -1)
        if idx == -1: return

        new_idx = idx + direction
        if 0 <= new_idx < len(self.image_items):
            # Swap in list
            self.image_items[idx], self.image_items[new_idx] = self.image_items[new_idx], self.image_items[idx]
            self.refresh_ui_order()

    def remove_item(self, filepath):
        idx = next((i for i, item in enumerate(self.image_items) if item['path'] == filepath), -1)
        if idx != -1:
            item = self.image_items.pop(idx)
            item['frame'].destroy()
            self.refresh_ui_order()

    def refresh_ui_order(self):
        for i, item in enumerate(self.image_items):
            item['frame'].grid(row=i, column=0, sticky="ew", padx=10, pady=8)
            # Update button states
            item['btn_up'].configure(state="normal" if i > 0 else "disabled")
            item['btn_down'].configure(state="normal" if i < len(self.image_items) - 1 else "disabled")

    def clear_all(self):
        for item in self.image_items:
            item['frame'].destroy()
        self.image_items.clear()

    def process_image_for_pdf(self, path, quality_setting):
        img = Image.open(path)
        original_format = img.format or "JPEG"
        if original_format.upper() not in ["JPEG", "PNG"]:
            original_format = "JPEG"
        
        # Determine scale and quality
        if quality_setting == "Low":
            scale = 0.25
            jpeg_quality = 25
        elif quality_setting == "Medium":
            scale = 0.50
            jpeg_quality = 50
        else: # High
            scale = 0.75
            jpeg_quality = 75

        # Resize image proportionally
        if scale < 1.0:
            new_width = max(1, int(img.width * scale))
            new_height = max(1, int(img.height * scale))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # Ensure correct mode for JPEG
        if original_format == "JPEG" and img.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode in ('RGBA', 'LA'):
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
            
        # Save to memory in the appropriate format
        b = io.BytesIO()
        if original_format == "JPEG":
            img.save(b, format="JPEG", quality=jpeg_quality, optimize=True)
        else:
            img.save(b, format="PNG", optimize=True)
            
        return b.getvalue()

    def convert_to_pdf(self):
        if not self.image_items:
            messagebox.showwarning("Warning", "No images to convert!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not save_path:
            return

        quality_setting = self.quality_optionmenu.get()

        try:
            image_inputs = []
            
            for item in self.image_items:
                path = item['path']
                if quality_setting == "Lossless":
                    image_inputs.append(path)
                else:
                    img_bytes = self.process_image_for_pdf(path, quality_setting)
                    image_inputs.append(img_bytes)
            
            if image_inputs:
                try:
                    with open(save_path, "wb") as f:
                        f.write(img2pdf.convert(image_inputs))
                    messagebox.showinfo("Success", f"Converted {len(image_inputs)} images to PDF!\nQuality: {quality_setting}\n\nSaved at: {save_path}")
                    return
                except Exception as img2pdf_err:
                    print(f"img2pdf failed. Falling back to Pillow: {img2pdf_err}")
            
            # --- FALLBACK using Pillow (only hits here if Lossless had an unsupported format like BMP) ---
            processed_images = []
            for item in self.image_items:
                img = Image.open(item['path'])
                if img.mode != 'RGB':
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        bg.paste(img, mask=img.split()[-1])
                    else:
                        bg.paste(img)
                    img = bg
                processed_images.append(img)
            
            if processed_images:
                save_kwargs = {
                    "resolution": 100.0,
                    "save_all": True,
                    "append_images": processed_images[1:]
                }
                
                if quality_setting == "Lossless":
                    save_kwargs["quality"] = 100
                    save_kwargs["subsampling"] = 0
                else:
                    save_kwargs["quality"] = 90 if quality_setting == "High" else (75 if quality_setting == "Medium" else 50)
                
                processed_images[0].save(save_path, "PDF", **save_kwargs)
                messagebox.showinfo("Success", f"Converted {len(processed_images)} images to PDF!\nQuality: {quality_setting}\n\nSaved at: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert:\n\n{str(e)}")

if __name__ == "__main__":
    app = ImgToPdfApp()
    app.mainloop()
