import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from config import FILE_PATTERNS
from tkinter import simpledialog

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager App")
        
        self.file_patterns = FILE_PATTERNS
        
        self.create_widgets()
        
    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        self.select_folder_btn = tk.Button(self.frame, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.pattern_var = tk.StringVar()
        self.pattern_var.set(".zip")
        self.pattern_menu = tk.OptionMenu(self.frame, self.pattern_var, *self.file_patterns)
        self.pattern_menu.grid(row=0, column=1, padx=5, pady=5)
        
        self.rename_btn = tk.Button(self.frame, text="Rename", command=self.rename_files)
        self.rename_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.move_btn = tk.Button(self.frame, text="Move", command=self.move_files)
        self.move_btn.grid(row=0, column=3, padx=5, pady=5)
        
        self.delete_btn = tk.Button(self.frame, text="Delete", command=self.delete_files)
        self.delete_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.current_folder = folder_selected
            self.refresh_file_list()
            
    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        files = [f for f in os.listdir(self.current_folder) if f.endswith(self.pattern_var.get())]
        for file in files:
            self.file_listbox.insert(tk.END, file)
            
    def rename_files(self):
        selected_files = self.file_listbox.curselection()
        if not selected_files:
            messagebox.showwarning("Rename Files", "Please select files to rename.")
            return
        for index in selected_files:
            file_name = self.file_listbox.get(index)
            new_name = simpledialog.askstring("Rename File", f"Enter new name for {file_name}:")
            if new_name:
                old_path = os.path.join(self.current_folder, file_name)
                new_path = os.path.join(self.current_folder, new_name)
                os.rename(old_path, new_path)
        self.refresh_file_list()

    def move_files(self):
        selected_files = self.file_listbox.curselection()
        destination_folder = filedialog.askdirectory()
        if destination_folder:
            for index in selected_files:
                file_name = self.file_listbox.get(index)
                old_path = os.path.join(self.current_folder, file_name)
                new_path = os.path.join(destination_folder, file_name)
                os.rename(old_path, new_path)
            self.refresh_file_list()
        
    def delete_files(self):
        selected_files = self.file_listbox.curselection()
        if messagebox.askyesno("Delete Files", "Are you sure you want to delete selected files?"):
            for index in selected_files:
                file_name = self.file_listbox.get(index)
                file_path = os.path.join(self.current_folder, file_name)
                os.remove(file_path)
            self.refresh_file_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
