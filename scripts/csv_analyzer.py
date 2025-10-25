
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CSVAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de CSV")

        self.dataframe = None
        self.file_path = "sample.csv" # Default to sample.csv

        self.create_widgets()
        self.load_csv(self.file_path)

    def create_widgets(self):
        # Frame para botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        load_button = tk.Button(button_frame, text="Carregar CSV", command=self.load_csv_dialog)
        load_button.pack(side=tk.LEFT, padx=5)

        # Frame para filtros
        filter_frame = tk.LabelFrame(self.root, text="Filtros")
        filter_frame.pack(pady=10, padx=10, fill=tk.X)

        self.filter_entries = {}
        self.filter_vars = {}

        # Tabela para exibir os dados
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars para a tabela
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

    def load_csv_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.load_csv(self.file_path)

    def load_csv(self, file_path):
        try:
            self.dataframe = pd.read_csv(file_path)
            self.display_data()
            self.create_filter_widgets()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o arquivo CSV: {e}")
            self.dataframe = None

    def create_filter_widgets(self):
        # Limpar filtros existentes
        for widget in self.filter_entries.values():
            widget.destroy()
        self.filter_entries.clear()
        self.filter_vars.clear()

        filter_frame = self.root.children["labelframe"] # Acessa o LabelFrame de filtros
        for i, col in enumerate(self.dataframe.columns):
            lbl = tk.Label(filter_frame, text=f"{col}:")
            lbl.grid(row=0, column=i*2, padx=5, pady=5, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(filter_frame, textvariable=var)
            entry.grid(row=0, column=i*2+1, padx=5, pady=5, sticky="ew")
            entry.bind("<KeyRelease>", self.apply_filters)

            self.filter_entries[col] = entry
            self.filter_vars[col] = var
        
        filter_frame.grid_columnconfigure("all", weight=1)

    def display_data(self, filtered_df=None):
        # Limpar a tabela existente
        for item in self.tree.get_children():
            self.tree.delete(item)

        if filtered_df is None:
            df_to_display = self.dataframe
        else:
            df_to_display = filtered_df

        if df_to_display is not None:
            # Definir colunas
            self.tree["columns"] = list(df_to_display.columns)
            self.tree["show"] = "headings"

            for col in df_to_display.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")

            # Inserir dados
            for index, row in df_to_display.iterrows():
                self.tree.insert("", "end", values=list(row))

    def apply_filters(self, event=None):
        if self.dataframe is None:  return

        filtered_df = self.dataframe.copy()
        for col, var in self.filter_vars.items():
            filter_value = var.get().strip()
            if filter_value:
                # Filtro case-insensitive e parcial
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(filter_value, case=False, na=False)]
        
        self.display_data(filtered_df)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAnalyzerApp(root)
    root.mainloop()

