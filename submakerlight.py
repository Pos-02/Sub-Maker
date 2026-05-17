import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

class UE4SSModCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UE4SS Mod Template Creator")
        self.root.geometry("650x520")
        self.root.minsize(550, 450)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.detected_paths = []
        self.include_config_var = ctk.BooleanVar(value=True)
        
        self.setup_ui()
        self.path_entry.insert(0, r"G:\SteamLibrary")
        self.scan_library()

    def setup_ui(self):
        path_frame = ctk.CTkFrame(self.root)
        path_frame.pack(fill="x", padx=15, pady=10)
        
        path_label = ctk.CTkLabel(path_frame, text="Steam Library Path", font=("Segoe UI", 12, "bold"))
        path_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        path_row = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_row.pack(fill="x", padx=5, pady=5)
        
        self.path_entry = ctk.CTkEntry(path_row)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ctk.CTkButton(path_row, text="Browse...", width=90, command=self.browse_folder)
        browse_btn.pack(side="left", padx=5)
        
        scan_btn = ctk.CTkButton(path_row, text="Scan", width=90, command=self.scan_library)
        scan_btn.pack(side="left")

        list_frame = ctk.CTkFrame(self.root)
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        list_label = ctk.CTkLabel(list_frame, text="Detected UE4SS Games", font=("Segoe UI", 12, "bold"))
        list_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        self.games_textbox = ctk.CTkTextbox(list_frame, font=("Segoe UI", 11), activate_scrollbars=True)
        self.games_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.games_textbox.configure(cursor="arrow")
        self.games_textbox.bind("<Button-1>", self.on_textbox_click)

        mod_frame = ctk.CTkFrame(self.root)
        mod_frame.pack(fill="x", padx=15, pady=10)
        
        mod_label = ctk.CTkLabel(mod_frame, text="New Mod Details", font=("Segoe UI", 12, "bold"))
        mod_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        name_row = ctk.CTkFrame(mod_frame, fg_color="transparent")
        name_row.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(name_row, text="Mod Name:").pack(side="left", padx=(5, 5))
        
        self.mod_name_entry = ctk.CTkEntry(name_row)
        self.mod_name_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.mod_name_entry.insert(0, "MyCoolMod")
        
        options_row = ctk.CTkFrame(mod_frame, fg_color="transparent")
        options_row.pack(fill="x", padx=5, pady=5)
        
        config_chk = ctk.CTkCheckBox(options_row, text="Include config.lua", variable=self.include_config_var)
        config_chk.pack(side="left", padx=5)
        
        create_btn = ctk.CTkButton(options_row, text="Create Template", command=self.create_template)
        create_btn.pack(side="right", padx=(5, 0))

    def browse_folder(self):
        selected_dir = filedialog.askdirectory(initialdir=self.path_entry.get())
        if selected_dir:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, os.path.normpath(selected_dir))
            self.scan_library()

    def scan_library(self):
        self.games_textbox.configure(state="normal")
        self.games_textbox.delete("1.0", "end")
        self.detected_paths = []
        
        steam_library = self.path_entry.get().strip()
        base_path = Path(steam_library) / "steamapps" / "common"
        
        if not base_path.exists():
            self.games_textbox.insert("end", "❌ Invalid path - Steam library not found")
            self.games_textbox.configure(state="disabled")
            return

        try:
            for game_dir in base_path.iterdir():
                if game_dir.is_dir():
                    for mods_path in game_dir.rglob("Binaries/Win64/ue4ss/Mods"):
                        if mods_path.is_dir():
                            self.detected_paths.append(mods_path)
                            game_name = mods_path.parts[mods_path.parts.index("common") + 1]
                            self.games_textbox.insert("end", f" 🎮 {game_name}\n")
        except Exception as e:
            self.games_textbox.insert("end", f"❌ Error scanning: {str(e)}")
            self.games_textbox.configure(state="disabled")
            return

        if not self.detected_paths:
            self.games_textbox.insert("end", "No UE4SS installations found. Check path or scan again.")
        
        self.games_textbox.configure(state="disabled")

    def on_textbox_click(self, event):
        self.games_textbox.tag_remove("highlight", "1.0", "end")
        line_index = self.games_textbox.index(f"@{event.x},{event.y}").split('.')[0]
        
        line_content = self.games_textbox.get(f"{line_index}.0", f"{line_index}.end").strip()
        if not line_content or "❌" in line_content or "No UE4SS" in line_content:
            self.selected_line_idx = None
            return
            
        self.selected_line_idx = int(line_index) - 1
        if self.selected_line_idx < len(self.detected_paths):
            self.games_textbox.tag_add("highlight", f"{line_index}.0", f"{line_index}.end")
            self.games_textbox.tag_config("highlight", background="#264f78")

    def create_template(self):
        if not hasattr(self, 'selected_line_idx') or self.selected_line_idx is None or not self.detected_paths:
            messagebox.showwarning("Warning", "Please click to select a game from the list first.")
            return
        
        if self.selected_line_idx >= len(self.detected_paths):
            messagebox.showwarning("Warning", "Please select a valid game from the list.")
            return
            
        target_mods_dir = self.detected_paths[self.selected_line_idx]
        
        mod_name = self.mod_name_entry.get().strip()
        if not mod_name:
            messagebox.showwarning("Warning", "Mod Name cannot be empty.")
            return
            
        for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
            mod_name = mod_name.replace(char, '')

        mod_root = target_mods_dir / mod_name
        scripts_dir = mod_root / "scripts"
        
        try:
            scripts_dir.mkdir(parents=True, exist_ok=True)
            
            with open(scripts_dir / "main.lua", "w", encoding="utf-8") as f:
                f.write(f"-- {mod_name} - Main Script\nprint('[*] Hello from inside {mod_name}!')\n")
                
            if self.include_config_var.get():
                with open(scripts_dir / "config.lua", "w", encoding="utf-8") as f:
                    f.write(f"-- {mod_name} - Configuration\nconfig = {{\n    enabled = true\n}}\n")
                
            with open(mod_root / "enabled.txt", "w", encoding="utf-8") as f:
                f.write("") 
                
            messagebox.showinfo("Success!", f"Successfully created mod folder tree for '{mod_name}'!\n\nLocation:\n{mod_root}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the tree:\n{str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = UE4SSModCreatorGUI(root)
    root.mainloop()