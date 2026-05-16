import os
import string
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, is_error=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x200")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color="#1e1e24")
        
        main_frame = ctk.CTkFrame(self, fg_color="#2a2a32", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        accent_color = "#e74c3c" if is_error else "#2ecc71"
        badge_text = "Error" if is_error else "Success"
        
        badge_label = ctk.CTkLabel(
            main_frame, 
            text=badge_text, 
            font=ctk.CTkFont(size=28),
            text_color=accent_color
        )
        badge_label.pack(pady=(15, 5))
        
        msg_label = ctk.CTkLabel(
            main_frame, 
            text=message, 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            wraplength=380,
            text_color="#f5f5f5"
        )
        msg_label.pack(fill="both", expand=True, padx=20, pady=5)
        
        btn_color = "#3a3a44" if is_error else "#007acc"
        btn_hover = "#4a4a55" if is_error else "#0098ff"
        
        ok_btn = ctk.CTkButton(
            main_frame, 
            text="Dismiss", 
            width=100,
            height=32,
            fg_color=btn_color,
            hover_color=btn_hover,
            command=self.destroy
        )
        ok_btn.pack(pady=(5, 15))
        
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        p_x = parent.winfo_x()
        p_y = parent.winfo_y()
        p_w = parent.winfo_width()
        p_h = parent.winfo_height()
        
        x = p_x + (p_w // 2) - (self.winfo_width() // 2)
        y = p_y + (p_h // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

class CustomConfirmBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("480x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color="#1e1e24")
        
        self.result = False
        
        main_frame = ctk.CTkFrame(self, fg_color="#2a2a32", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        badge_label = ctk.CTkLabel(main_frame, text="❓", font=ctk.CTkFont(size=28))
        badge_label.pack(pady=(15, 5))
        
        msg_label = ctk.CTkLabel(
            main_frame, 
            text=message, 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            wraplength=400,
            text_color="#f5f5f5"
        )
        msg_label.pack(fill="both", expand=True, padx=20, pady=5)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(5, 15))
        
        no_btn = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            width=90,
            height=32,
            fg_color="#3a3a44",
            hover_color="#4a4a55",
            command=self.on_no
        )
        no_btn.pack(side="left", padx=10)
        
        yes_btn = ctk.CTkButton(
            btn_frame, 
            text="Create", 
            width=90,
            height=32,
            fg_color="#007acc",
            hover_color="#0098ff",
            command=self.on_yes
        )
        yes_btn.pack(side="left", padx=10)
        
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        p_x = parent.winfo_x()
        p_y = parent.winfo_y()
        p_w = parent.winfo_width()
        p_h = parent.winfo_height()
        
        x = p_x + (p_w // 2) - (self.winfo_width() // 2)
        y = p_y + (p_h // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()

class Subnautica2ModCreator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SubMaker - UE4SS Mod Creator")
        self.geometry("850x700")
        self.minsize(750, 600)

        self.default_mod_dir = self.detect_subnautica_dir()
        self.default_main_lua = (
            "-- Subnautica 2 UE4SS Mod\n\n"
            "-- This is the main script for your mod. It will be executed when the game loads\n\n"
            "end)\n"
        )
        self.default_config_lua = (
            "-- Configuration for [ModName]\n\n"
            "config = {\n"
            "--this is where you can define custom settings for your mod, which can be accessed in main.lua\n"
            "}\n\n"
            "return config\n"
        )

        self.setup_ui()

    def detect_subnautica_dir(self):
        path_suffix = os.path.join("SteamLibrary", "steamapps", "common", "Subnautica2", "Subnautica2", "Binaries", "Win64", "ue4ss", "Mods")
        available_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        
        for drive in available_drives:
            full_path = os.path.join(drive, path_suffix)
            if os.path.exists(full_path):
                return full_path
                
        fallback_path = os.path.join("C:\\", "Program Files (x86)", "Steam", "steamapps", "common", "Subnautica2", "Subnautica2", "Binaries", "Win64", "ue4ss", "Mods")
        if os.path.exists(fallback_path):
            return fallback_path

        return os.path.expanduser("~")

    def setup_ui(self):
        header_label = ctk.CTkLabel(self, text="SUBMAKER", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        header_label.pack(anchor="w", padx=20, pady=(20, 10))

        config_frame = ctk.CTkFrame(self, corner_radius=10)
        config_frame.pack(fill="x", padx=20, pady=10)

        name_label = ctk.CTkLabel(config_frame, text="Mod Name:", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        name_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        self.mod_name_entry = ctk.CTkEntry(config_frame, placeholder_text="ExampleName", width=250)
        self.mod_name_entry.insert(0, "ExampleName")
        self.mod_name_entry.grid(row=0, column=1, sticky="w", padx=15, pady=(15, 5))

        path_label = ctk.CTkLabel(config_frame, text="UE4SS Mods Path:", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        path_label.grid(row=1, column=0, sticky="w", padx=15, pady=5)

        self.dir_entry = ctk.CTkEntry(config_frame, placeholder_text="Path to UE4SS Mods folder")
        self.dir_entry.insert(0, self.default_mod_dir)
        self.dir_entry.grid(row=1, column=1, sticky="ew", padx=15, pady=5)

        browse_btn = ctk.CTkButton(config_frame, text="Browse", width=100, fg_color="#3a3a44", hover_color="#4a4a55", command=self.browse_dir)
        browse_btn.grid(row=1, column=2, padx=15, pady=5)
        
        config_frame.columnconfigure(1, weight=1)

        if self.default_mod_dir != os.path.expanduser("~"):
            status_msg = "Path automatically discovered!"
            status_color = "#2ecc71"
        else:
            status_msg = "Direct path not found. Please locate it manually."
            status_color = "orange"

        self.path_status_lbl = ctk.CTkLabel(config_frame, text=status_msg, font=ctk.CTkFont(size=11, slant="italic"), text_color=status_color)
        self.path_status_lbl.grid(row=2, column=1, sticky="w", padx=15, pady=(0, 15))

        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tabview.add(" main.lua ")
        self.tabview.add(" config.lua ")

        def build_editor(tab_name, template_text):
            parent_tab = self.tabview.tab(tab_name)
            textbox = ctk.CTkTextbox(
                parent_tab, 
                font=("Consolas", 12), 
                text_color="#e0e0e0",
                fg_color="#121214",
                border_width=1,
                border_color="#2a2a32",
                activate_scrollbars=True
            )
            textbox.pack(fill="both", expand=True, padx=5, pady=5)
            textbox.insert("1.0", template_text.replace("[ModName]", "MyAwesomeMod"))
            return textbox

        self.main_lua_text = build_editor(" main.lua ", self.default_main_lua)
        self.config_lua_text = build_editor(" config.lua ", self.default_config_lua)

        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.status_var = tk.StringVar(value="System ready.")
        status_lbl = ctk.CTkLabel(footer_frame, textvariable=self.status_var, font=ctk.CTkFont(size=12), text_color="#aaaaaa")
        status_lbl.pack(side="left", anchor="center")

        build_btn = ctk.CTkButton(
            footer_frame, 
            text="Build Mod Structure", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.create_mod
        )
        build_btn.pack(side="right", anchor="center")

    def browse_dir(self):
        selected_dir = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if selected_dir:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, selected_dir)
            self.path_status_lbl.configure(text="Path set manually.", text_color="#3498db")

    def show_custom_message(self, title, message, is_error=False):
        CustomMessageBox(self, title, message, is_error)

    def show_custom_confirm(self, title, message):
        dialog = CustomConfirmBox(self, title, message)
        self.wait_window(dialog)
        return dialog.result

    def create_mod(self):
        mod_name = self.mod_name_entry.get().strip()
        base_mods_dir = self.dir_entry.get().strip()

        if not mod_name:
            self.show_custom_message("Error", "Please input a valid name for your mod.", is_error=True)
            return

        if not os.path.exists(base_mods_dir):
            msg = f"Target directory not found:\n{base_mods_dir}\n\nCreate it?"
            if self.show_custom_confirm("Directory Missing", msg):
                os.makedirs(base_mods_dir, exist_ok=True)
            else:
                return

        mod_root = os.path.join(base_mods_dir, mod_name)
        scripts_dir = os.path.join(mod_root, "scripts")

        try:
            os.makedirs(scripts_dir, exist_ok=True)

            with open(os.path.join(scripts_dir, "main.lua"), "w", encoding="utf-8") as f:
                f.write(self.main_lua_text.get("1.0", "end").strip())

            with open(os.path.join(scripts_dir, "config.lua"), "w", encoding="utf-8") as f:
                f.write(self.config_lua_text.get("1.0", "end").strip())

            with open(os.path.join(mod_root, "enabled.txt"), "w", encoding="utf-8") as f:
                f.write("")

            self.status_var.set(f"Compiled successfully: {mod_name}")
            self.show_custom_message("Success", f"Mod environment generated cleanly at:\n{mod_root}")

        except Exception as e:
            self.status_var.set("Compilation failed.")
            self.show_custom_message("I/O Error", f"Failed to construct mod folder hierarchy: {str(e)}", is_error=True)

if __name__ == "__main__":
    app = Subnautica2ModCreator()
    app.mainloop()