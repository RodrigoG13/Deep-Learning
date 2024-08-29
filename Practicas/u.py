import tkinter as tk
from tkinter import filedialog, messagebox, Text
from tkinter.font import Font
import subprocess
import os

class LaTeXEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de LaTeX")
        
        # Área de texto (debe inicializarse antes de crear el menú)
        self.text_area = Text(root, wrap='none', undo=True, font=Font(family="Courier", size=12))
        self.text_area.pack(fill='both', expand=1)
        self.text_area.bind('<KeyRelease>', self.on_key_release)
        
        # Crear el menú
        self.create_menu()
        
        # Barra de estado
        self.status_bar = tk.Label(root, text="Bienvenido al Editor de LaTeX", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Vista previa del PDF
        self.pdf_preview = tk.Label(root)
        self.pdf_preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Botón para compilar
        self.compile_button = tk.Button(root, text="Compilar LaTeX", command=self.compile_latex)
        self.compile_button.pack()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Deshacer", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Rehacer", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cortar", command=lambda: self.text_area.event_generate('<<Cut>>'), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copiar", command=lambda: self.text_area.event_generate('<<Copy>>'), accelerator="Ctrl+C")
        edit_menu.add_command(label="Pegar", command=lambda: self.text_area.event_generate('<<Paste>>'), accelerator="Ctrl+V")
        menubar.add_cascade(label="Editar", menu=edit_menu)
        
        self.root.config(menu=menubar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos LaTeX", "*.tex"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, file.read())
            self.status_bar.config(text=f"Archivo abierto: {file_path}")
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("Archivos LaTeX", "*.tex"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get("1.0", tk.END))
            self.status_bar.config(text=f"Archivo guardado: {file_path}")
    
    def compile_latex(self):
        latex_code = self.text_area.get("1.0", tk.END)
        
        # Guardar el código LaTeX en un archivo
        with open("documento.tex", "w") as file:
            file.write(latex_code)
        
        # Ejecutar el comando pdflatex para compilar el archivo LaTeX
        result = subprocess.run(["pdflatex", "documento.tex"], capture_output=True, text=True)
        
        if result.returncode == 0:
            self.status_bar.config(text="Documento compilado exitosamente")
            self.show_pdf_preview("documento.pdf")
        else:
            self.show_error_log(result.stderr)
    
    def show_error_log(self, log):
        log_window = tk.Toplevel(self.root)
        log_window.title("Log de Compilación")
        
        log_text = Text(log_window, wrap='word', width=100, height=30)
        log_text.pack(fill='both', expand=True)
        log_text.insert(tk.END, log)
        log_text.config(state=tk.DISABLED)
    
    def show_pdf_preview(self, pdf_path):
        if os.name == 'nt':  # Para Windows
            os.startfile(pdf_path)
        elif os.name == 'posix':  # Para Linux, macOS, etc.
            subprocess.run(["xdg-open", pdf_path])

    def on_key_release(self, event=None):
        self.highlight_syntax()

    def highlight_syntax(self):
        # Un resaltado de sintaxis muy básico
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        
        keywords = ["\\begin", "\\end", "\\section", "\\subsection"]
        for keyword in keywords:
            start = "1.0"
            while True:
                start = self.text_area.search(keyword, start, tk.END)
                if not start:
                    break
                end = f"{start}+{len(keyword)}c"
                self.text_area.tag_add("highlight", start, end)
                self.text_area.tag_config("highlight", foreground="blue")
                start = end

if __name__ == "__main__":
    root = tk.Tk()
    editor = LaTeXEditor(root)
    root.mainloop()
