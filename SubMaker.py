import os
import string
import re
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

VS_BG_DARK = "#1E1E1E"        
VS_PANEL_BG = "#252526"       
VS_EDITOR_BG = "#1D1D1D"      
VS_BORDER_COLOR = "#3F3F46"   
VS_ACCENT_BLUE = "#007ACC"    
VS_ACCENT_HOVER = "#1C97EA"   
VS_TEXT_WHITE = "#D4D4D4"     

COLOR_KEYWORD = "#569CD6"     
COLOR_BUILTIN = "#DCDCAA"     
COLOR_STRING = "#CE9178"      
COLOR_COMMENT = "#6A9955"     
COLOR_NUMBER = "#B5CEA8"      
COLOR_GUTTER_TEXT = "#858585" 

class CodeEditorWithGutter(ctk.CTkFrame):
    def __init__(self, parent, template_text):
        super().__init__(parent, fg_color=VS_EDITOR_BG, corner_radius=2, border_width=1, border_color=VS_BORDER_COLOR)

        self.gutter = tk.Text(
            self, width=4, padx=5, pady=5, 
            font=("Consolas", 13), bg=VS_PANEL_BG, fg=COLOR_GUTTER_TEXT, 
            bd=0, highlightthickness=0, state="disabled", insertbackground=VS_PANEL_BG
        )
        self.gutter.pack(side="left", fill="y")

        self.textbox = tk.Text(
            self, wrap="none", font=("Consolas", 13), 
            bg=VS_EDITOR_BG, fg=VS_TEXT_WHITE, bd=0, 
            highlightthickness=0, padx=5, pady=5, undo=True, maxundo=50,
            insertbackground=VS_TEXT_WHITE  
        )
        self.textbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self, command=self.on_scroll, orientation="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.gutter.config(yscrollcommand=self.scrollbar.set)

        self.setup_tags()

        self.textbox.insert("1.0", template_text)

        self.textbox.bind("<KeyRelease>", self.on_content_changed)
        self.textbox.bind("<MouseWheel>", self.sync_scroll)
        self.textbox.bind("<Button-1>", self.sync_scroll)
        
        self.update_syntax_highlighting()
        self.update_line_numbers()

    def setup_tags(self):
        self.textbox.tag_configure("keyword", foreground=COLOR_KEYWORD)
        self.textbox.tag_configure("builtin", foreground=COLOR_BUILTIN)
        self.textbox.tag_configure("string", foreground=COLOR_STRING)
        self.textbox.tag_configure("comment", foreground=COLOR_COMMENT)
        self.textbox.tag_configure("number", foreground=COLOR_NUMBER)

    def on_scroll(self, *args):
        self.textbox.yview(*args)
        self.gutter.yview(*args)

    def sync_scroll(self, event=None):
        self.gutter.yview_moveto(self.textbox.yview()[0])

    def on_content_changed(self, event=None):
        self.update_syntax_highlighting()
        self.update_line_numbers()
        self.sync_scroll()

    def update_line_numbers(self):
        self.gutter.config(state="normal")
        self.gutter.delete("1.0", "end")
        
        line_count = int(self.textbox.index('end-1c').split('.')[0])
        gutter_content = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.gutter.insert("1.0", gutter_content)
        self.gutter.config(state="disabled")

    def update_syntax_highlighting(self):
        for tag in ["keyword", "builtin", "string", "comment", "number"]:
            self.textbox.tag_remove(tag, "1.0", "end")

        content = self.textbox.get("1.0", "end-1c")

        rules = [
            ("comment", r"--.*"),
            ("string", r"\"[^\"]*\"|'[^']*'"),
            ("keyword", r"\b(and|break|do|else|elseif|end|false|for|function|if|in|local|nil|not|or|repeat|return|then|true|until|while)\b"),
            ("builtin", r"\b(print|require|pairs|ipairs|table|string|math|os|io|Vector|Rotator|StaticFindObject|NotifyOnHook)\b"),
            ("number", r"\b\d+(\.\d+)?\b")
        ]

        for tag_name, pattern in rules:
            for match in re.finditer(pattern, content):
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                self.textbox.tag_add(tag_name, start_index, end_index)


class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, is_error=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=VS_BG_DARK)
        
        main_frame = ctk.CTkFrame(self, fg_color=VS_PANEL_BG, corner_radius=4, border_width=1, border_color=VS_BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        accent_color = "#F14C4C" if is_error else "#89D185"
        badge_text = "Error" if is_error else "Success"
        
        badge_label = ctk.CTkLabel(main_frame, text=badge_text, font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=accent_color)
        badge_label.pack(pady=(20, 5))
        
        msg_label = ctk.CTkLabel(main_frame, text=message, font=ctk.CTkFont(family="Segoe UI", size=13), wraplength=380, text_color=VS_TEXT_WHITE)
        msg_label.pack(fill="both", expand=True, padx=20, pady=5)
        
        btn_color = "#3A3A3C" if is_error else VS_ACCENT_BLUE
        btn_hover = "#4A4A4C" if is_error else VS_ACCENT_HOVER
        
        ok_btn = ctk.CTkButton(main_frame, text="Dismiss", width=100, height=30, corner_radius=2, fg_color=btn_color, hover_color=btn_hover, command=self.destroy)
        ok_btn.pack(pady=(5, 15))
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class CustomConfirmBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("480x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=VS_BG_DARK)
        
        self.result = False
        main_frame = ctk.CTkFrame(self, fg_color=VS_PANEL_BG, corner_radius=4, border_width=1, border_color=VS_BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        badge_label = ctk.CTkLabel(main_frame, text="❓", font=ctk.CTkFont(size=24))
        badge_label.pack(pady=(15, 5))
        
        msg_label = ctk.CTkLabel(main_frame, text=message, font=ctk.CTkFont(family="Segoe UI", size=13), wraplength=400, text_color=VS_TEXT_WHITE)
        msg_label.pack(fill="both", expand=True, padx=20, pady=5)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(5, 15))
        
        no_btn = ctk.CTkButton(btn_frame, text="Cancel", width=90, height=30, corner_radius=2, fg_color="#3A3A3C", hover_color="#4A4A4C", command=self.on_no)
        no_btn.pack(side="left", padx=10)
        
        yes_btn = ctk.CTkButton(btn_frame, text="Create", width=90, height=30, corner_radius=2, fg_color=VS_ACCENT_BLUE, hover_color=VS_ACCENT_HOVER, command=self.on_yes)
        yes_btn.pack(side="left", padx=10)
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def on_yes(self): self.result = True; self.destroy()
    def on_no(self): self.result = False; self.destroy()


class ChangelogViewerWindow(ctk.CTkToplevel):
    def __init__(self, parent, text_content):
        super().__init__(parent)
        self.title("Mod Changelog (Read Only)")
        self.geometry("550x400")
        self.minsize(400, 300)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=VS_BG_DARK)

        title_label = ctk.CTkLabel(self, text="CHANGELOG.md", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#9CDCFE")
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.textbox = ctk.CTkTextbox(
            self, font=("Consolas", 12), text_color=VS_TEXT_WHITE,
            fg_color=VS_EDITOR_BG, border_width=1, border_color=VS_BORDER_COLOR,
            corner_radius=2, activate_scrollbars=True
        )
        self.textbox.pack(fill="both", expand=True, padx=20, pady=5)
        self.textbox.insert("1.0", text_content)
        self.textbox.configure(state="disabled")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", padx=20, pady=15)

        close_btn = ctk.CTkButton(btn_frame, text="Close", width=90, height=30, corner_radius=2, fg_color=VS_ACCENT_BLUE, hover_color=VS_ACCENT_HOVER, command=self.destroy)
        close_btn.pack(side="right")

        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class Subnautica2ModCreator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SubMaker - UE4SS Mod Creator")
        self.geometry("950x900")
        self.minsize(800, 800)
        self.configure(fg_color=VS_BG_DARK)

        self.default_mod_dir = self.detect_subnautica_dir()
        
        self.default_main_lua = (
            "-- This is your main.lua template. Write your mod's Lua code here."
        )
        self.default_config_lua = (
            "-- This is your config.lua template. Configure your mod's settings here."
        )
        
        self.changelog_data = (
            "# Changelog\n\n"
            "- Prettier GUI.\n"
            "- Added option to include config.lua.\n"
            "- Added ability to open mods folder."
        )

        self.setup_ui()

    def detect_subnautica_dir(self):
        path_suffix = os.path.join("SteamLibrary", "steamapps", "common", "Subnautica2", "Subnautica2", "Binaries", "Win64", "ue4ss", "Mods")
        available_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        for drive in available_drives:
            full_path = os.path.join(drive, path_suffix)
            if os.path.exists(full_path): return full_path
        return os.path.expanduser("~")

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color=VS_PANEL_BG, height=50, corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(header_frame, text="SUBMAKER // UE4SS MOD CREATOR", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#9CDCFE")
        header_label.pack(anchor="w", padx=20, side="left")

        config_frame = ctk.CTkFrame(self, fg_color=VS_PANEL_BG, corner_radius=4, border_width=1, border_color=VS_BORDER_COLOR)
        config_frame.pack(fill="x", padx=20, pady=20)

        name_label = ctk.CTkLabel(config_frame, text="Mod Name:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=VS_TEXT_WHITE)
        name_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.mod_name_entry = ctk.CTkEntry(config_frame, placeholder_text="ExampleModName", width=250, height=28, fg_color=VS_BG_DARK, border_color=VS_BORDER_COLOR, text_color=VS_TEXT_WHITE, corner_radius=2)
        self.mod_name_entry.insert(0, "ExampleName")
        self.mod_name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=(20, 5))

        self.include_config_var = tk.BooleanVar(value=True)
        self.config_checkbox = ctk.CTkCheckBox(config_frame, text="Include config.lua", variable=self.include_config_var, command=self.toggle_config_tab, font=ctk.CTkFont(family="Segoe UI", size=12), text_color=VS_TEXT_WHITE, fg_color=VS_ACCENT_BLUE, hover_color=VS_ACCENT_HOVER, corner_radius=2)
        self.config_checkbox.grid(row=0, column=2, sticky="w", padx=20, pady=(20, 5))

        path_label = ctk.CTkLabel(config_frame, text="UE4SS Mods Path:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=VS_TEXT_WHITE)
        path_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        self.dir_entry = ctk.CTkEntry(config_frame, placeholder_text="Path to UE4SS Mods folder", height=28, fg_color=VS_BG_DARK, border_color=VS_BORDER_COLOR, text_color=VS_TEXT_WHITE, corner_radius=2)
        self.dir_entry.insert(0, self.default_mod_dir)
        self.dir_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        browse_btn = ctk.CTkButton(config_frame, text="Browse...", width=90, height=28, corner_radius=2, fg_color="#3A3A3C", hover_color="#4A4A4C", text_color=VS_TEXT_WHITE, command=self.browse_dir)
        browse_btn.grid(row=1, column=3, padx=20, pady=5)
        config_frame.columnconfigure(1, weight=1)

        status_msg, status_color = ("Path automatically set!", "#89D185") if self.default_mod_dir != os.path.expanduser("~") else ("⚠ Direct path not found. Please locate it manually.", "#CCA700")
        self.path_status_lbl = ctk.CTkLabel(config_frame, text=status_msg, font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"), text_color=status_color)
        self.path_status_lbl.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=(0, 20))

        self.tabview = ctk.CTkTabview(
            self, corner_radius=4, fg_color=VS_PANEL_BG,
            segmented_button_fg_color=VS_BG_DARK, segmented_button_selected_color=VS_PANEL_BG,
            segmented_button_unselected_color=VS_BG_DARK, text_color=VS_TEXT_WHITE
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.tabview.add(" main.lua ")
        self.tabview.add(" config.lua ")

        self.main_lua_editor = CodeEditorWithGutter(self.tabview.tab(" main.lua "), self.default_main_lua)
        self.main_lua_editor.pack(fill="both", expand=True, padx=5, pady=5)

        self.config_lua_editor = CodeEditorWithGutter(self.tabview.tab(" config.lua "), self.default_config_lua)
        self.config_lua_editor.pack(fill="both", expand=True, padx=5, pady=5)

        footer_frame = ctk.CTkFrame(self, fg_color=VS_PANEL_BG, height=45, corner_radius=0)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        open_folder_btn = ctk.CTkButton(
            footer_frame, 
            text="Open Mods Folder", 
            font=ctk.CTkFont(family="Segoe UI", size=12), 
            height=45, 
            width=140, 
            corner_radius=0, 
            fg_color="#3A3A3C", 
            hover_color="#4A4A4C", 
            text_color=VS_TEXT_WHITE, 
            command=self.open_mods_folder
        )
        open_folder_btn.pack(side="left")

        changelog_btn = ctk.CTkButton(
            footer_frame,
            text="View Changelog",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=45,
            width=120,
            corner_radius=0,
            fg_color="#2D2D30",
            hover_color="#3F3F46",
            text_color=VS_TEXT_WHITE,
            command=self.open_changelog_window
        )
        changelog_btn.pack(side="left", padx=1)

        build_btn = ctk.CTkButton(footer_frame, text="Build Mod Structure", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), height=45, width=160, corner_radius=0, fg_color=VS_ACCENT_BLUE, hover_color=VS_ACCENT_HOVER, text_color="#FFFFFF", command=self.create_mod)
        build_btn.pack(side="right")

    def toggle_config_tab(self):
        if self.include_config_var.get():
            try:
                self.tabview.add(" config.lua ")
                self.config_lua_text_widget = CodeEditorWithGutter(self.tabview.tab(" config.lua "), self.default_config_lua)
                self.config_lua_text_widget.pack(fill="both", expand=True, padx=5, pady=5)
            except ValueError: pass
        else:
            try: self.tabview.delete(" config.lua ")
            except ValueError: pass

    def browse_dir(self):
        selected_dir = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if selected_dir:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, selected_dir)
            self.path_status_lbl.configure(text="Path configured manually.", text_color="#3794D5")

    def open_mods_folder(self):
        target_dir = self.dir_entry.get().strip()
        if os.path.exists(target_dir):
            os.startfile(target_dir)
        else:
            self.show_custom_message("Error", "The specified path does not exist.", is_error=True)

    def open_changelog_window(self):
        ChangelogViewerWindow(self, self.changelog_data)

    def show_custom_message(self, title, message, is_error=False): CustomMessageBox(self, title, message, is_error)
    def show_custom_confirm(self, title, message): dialog = CustomConfirmBox(self, title, message); self.wait_window(dialog); return dialog.result

    def create_mod(self):
        mod_name = self.mod_name_entry.get().strip()
        base_mods_dir = self.dir_entry.get().strip()

        if not mod_name:
            self.show_custom_message("Error", "Please input a valid name for your mod.", is_error=True)
            return

        if not os.path.exists(base_mods_dir):
            if self.show_custom_confirm("Directory Missing", f"Target environment directory not found:\n{base_mods_dir}\n\nInitialize hierarchy?"):
                os.makedirs(base_mods_dir, exist_ok=True)
            else: return

        mod_root = os.path.join(base_mods_dir, mod_name)
        scripts_dir = os.path.join(mod_root, "scripts")

        try:
            os.makedirs(scripts_dir, exist_ok=True)

            with open(os.path.join(scripts_dir, "main.lua"), "w", encoding="utf-8") as f:
                f.write(self.main_lua_editor.textbox.get("1.0", "end").strip())

            if self.include_config_var.get():
                with open(os.path.join(scripts_dir, "config.lua"), "w", encoding="utf-8") as f:
                    target_editor = getattr(self, 'config_lua_text_widget', self.config_lua_editor)
                    f.write(target_editor.textbox.get("1.0", "end").strip())
            else:
                old_config = os.path.join(scripts_dir, "config.lua")
                if os.path.exists(old_config): os.remove(old_config)

            with open(os.path.join(mod_root, "changelog.txt"), "w", encoding="utf-8") as f:
                f.write(self.changelog_data.strip())

            with open(os.path.join(mod_root, "enabled.txt"), "w", encoding="utf-8") as f: f.write("")
            self.show_custom_message("Success", f"Mod created successfully:\n{mod_root}")

        except Exception as e:
            self.show_custom_message("I/O File Error", f"Failed to construct mod folder hierarchy:\n{str(e)}", is_error=True)


if __name__ == "__main__":
    app = Subnautica2ModCreator()
    app.mainloop()