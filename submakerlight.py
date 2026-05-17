import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class UE4SSModCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UE4SS Mod Template Creator")
        self.root.geometry("650x480")
        self.root.minsize(550, 400)
        
        self.colors = {
            'bg': '#1e1e1e',           
            'fg': "#ffffff",         
            'frame_bg': '#252526',     
            'entry_bg': '#3c3c3c',     
            'button_bg': "#007acc",    
            'button_fg': "#FFFFFF",
            'button_hover': '#1c97ea', 
            'listbox_bg': '#1e1e1e',   
            'listbox_select': '#264f78', 
            'scrollbar_bg': '#3c3c3c', 
            'scrollbar_trough': '#1e1e1e', 
            'label_bg': '#252526',     
            'label_fg': "#000000",     
            'accent': '#569cd6',       
            'success': '#4ec9b0',      
            'warning': 'orange',      
            'error': 'red',        
        }
        
        self.detected_paths = []
        
        self.include_config_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.path_entry.insert(0, r"G:\SteamLibrary")
        self.scan_library()

    def setup_ui(self):
        self.setup_dark_mode_styles()
        
        path_frame = ttk.LabelFrame(self.root, text=" Steam Library Path ", padding=10)
        path_frame.pack(fill="x", padx=15, pady=10)
        
        self.path_entry = ttk.Entry(path_frame)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(path_frame, 
                               text="Browse...", 
                               command=self.browse_folder)
        browse_btn.pack(side="left", padx=5)
        
        scan_btn = ttk.Button(path_frame, 
                             text="Scan", 
                             command=self.scan_library)
        scan_btn.pack(side="left")

        list_frame = ttk.LabelFrame(self.root, text=" Detected UE4SS Games ", padding=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.games_listbox = tk.Listbox(list_frame, 
                                       yscrollcommand=scrollbar.set, 
                                       font=("Segoe UI", 10),
                                       bg=self.colors['listbox_bg'],
                                       fg=self.colors['fg'],
                                       selectbackground=self.colors['listbox_select'],
                                       selectforeground=self.colors['fg'],
                                       highlightthickness=0)
        self.games_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.games_listbox.yview)

        mod_frame = ttk.LabelFrame(self.root, text=" New Mod Details ", padding=10)
        mod_frame.pack(fill="x", padx=15, pady=10)
        
        name_row = ttk.Frame(mod_frame)
        name_row.pack(fill="x", pady=(0, 5))
        
        ttk.Label(name_row, text="Mod Name:").pack(side="left", padx=(0, 5))
        
        self.mod_name_entry = ttk.Entry(name_row)
        self.mod_name_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.mod_name_entry.insert(0, "MyCoolMod")
        
        options_row = ttk.Frame(mod_frame)
        options_row.pack(fill="x", pady=(5, 0))
        
        config_chk = ttk.Checkbutton(
            options_row, 
            text="Include config.lua", 
            variable=self.include_config_var
        )
        config_chk.pack(side="left", padx=5)
        
        create_btn = ttk.Button(options_row, 
                               text="Create Template", 
                               command=self.create_template)
        create_btn.pack(side="right", padx=(5, 0))

    def setup_dark_mode_styles(self):
        """Configure ttk styles for dark mode"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TLabel',
                       background=self.colors['label_bg'],
                       foreground=self.colors['label_fg'])
        
        style.configure('TFrame',
                       background=self.colors['frame_bg'])
        
        style.configure('TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       font=('Segoe UI', 10))
        
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['fg'],
                       insertcolor=self.colors['fg'])
        
        style.configure('TCheckbutton',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['fg'])
        
        style.configure('TLabelframe',
                       background=self.colors['frame_bg'])
        
        style.configure('TLabelframe.Label',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['fg'])
        
        style.configure('TScrollbar',
                       background=self.colors['scrollbar_bg'],
                       troughcolor=self.colors['scrollbar_trough'])
        
        self.root.configure(bg=self.colors['bg'])

    def browse_folder(self):
        selected_dir = filedialog.askdirectory(initialdir=self.path_entry.get())
        if selected_dir:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, os.path.normpath(selected_dir))
            self.scan_library()

    def scan_library(self):
        self.games_listbox.delete(0, tk.END)
        self.detected_paths = []
        
        steam_library = self.path_entry.get().strip()
        base_path = Path(steam_library) / "steamapps" / "common"
        
        if not base_path.exists():
            self.games_listbox.insert(tk.END, "❌ Invalid path - Steam library not found")
            return

        found_count = 0
        try:
            for game_dir in base_path.iterdir():
                if game_dir.is_dir():
                    for mods_path in game_dir.rglob("Binaries/Win64/ue4ss/Mods"):
                        if mods_path.is_dir():
                            self.detected_paths.append(mods_path)
                            game_name = mods_path.parts[mods_path.parts.index("common") + 1]
                            self.games_listbox.insert(tk.END, f" 🎮 {game_name}")
                            found_count += 1
        except Exception as e:
            self.games_listbox.insert(tk.END, f"❌ Error scanning: {str(e)}")
            return

        if not self.detected_paths:
            self.games_listbox.insert(tk.END, "No UE4SS installations found. Check path or scan again.")
        else:
            self.games_listbox.insert(tk.END, f"")

    def create_template(self):
        selection = self.games_listbox.curselection()
        if not selection or not self.detected_paths:
            messagebox.showwarning("Warning", "Please select a game from the list first.")
            return
        
        selected_index = selection[0]
        
        if selected_index >= len(self.detected_paths):
            messagebox.showwarning("Warning", "Please select a valid game from the list.")
            return
            
        target_mods_dir = self.detected_paths[selected_index]
        
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
    root = tk.Tk()
    app = UE4SSModCreatorGUI(root)
    root.mainloop()