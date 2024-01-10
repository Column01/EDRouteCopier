import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox

from route_copier import RouteCopier


class UI:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("ED Route Copier")
        self.master.geometry("600x400")
        self.journal_file_path = None
        self.route_file_path = None

        self.route_copier = None # Initialized when the "Load Route" button is clicked. See self.load_route

    def create_widgets(self) -> None:
        # Journal File Label
        self.label_journal = tk.Label(self.master, text="Latest Journal:", font=("Helvetica", 14, "bold", "underline"))
        self.label_journal.grid(row=0, column=0, padx=10, pady=10)
        # Display for file path
        self.entry_journal = tk.Entry(self.master, width=50, state="readonly")
        self.entry_journal.grid(row=0, column=1, sticky="EW", padx=10, pady=10)
        self.master.grid_columnconfigure(1, weight=1)
        # Browse Button
        self.browse_journal_button = tk.Button(self.master, text="Browse", command=self.browse_journal)
        self.browse_journal_button.grid(row=0, column=2, padx=10, pady=10)

        # Route File Label
        self.label_route = tk.Label(self.master, text="Neutron route CSV:", font=("Helvetica", 14, "bold", "underline"))
        self.label_route.grid(row=1, column=0, padx=10, pady=10)
        # Display for file path
        self.entry_route = tk.Entry(self.master, width=50, state="readonly")
        self.entry_route.grid(row=1, column=1, sticky="EW", padx=10, pady=10)
        self.master.grid_columnconfigure(1, weight=1)
        # Browse Button
        self.browse_route_button = tk.Button(self.master, text="Browse", command=self.browse_route)
        self.browse_route_button.grid(row=1, column=2, padx=10, pady=10)

        # Place holder button
        self.button = tk.Button(self.master, text="Load Route", command=self.load_route)
        self.button.grid(row=2, column=1, padx=10, pady=10)

    def browse_journal(self) -> None:
        path = self.get_journal_path()
        self.journal_file_path = filedialog.askopenfilename(title="Journal File", initialdir=path, filetypes=[("Journal Files", ".log")])
        if self.journal_file_path:
            self.populate_entry(self.entry_journal, self.journal_file_path)

    def browse_route(self) -> None:
        self.route_file_path = filedialog.askopenfilename(title="Route File", initialdir="/", filetypes=[("Route Files", ".csv")])
        if self.route_file_path:
            self.populate_entry(self.entry_route, self.route_file_path)

    def populate_entry(self, entry: tk.Entry, text: str) -> None:
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.configure(state="readonly")
    
    def get_journal_path(self) -> str:
        _platform = platform.system()
        if _platform == "Windows":
            user = os.environ.get("USERNAME")
            path = os.path.join("C:\\Users", user, "Saved Games\\Frontier Developments\\Elite Dangerous")
            if os.path.isdir(path):
                return path
            else:
                return "/"
        else:
            return "/"

    def load_route(self) -> None:
        if self.journal_file_path:
            if self.route_file_path:
                self.route_copier = RouteCopier(self.journal_file_path, self.route_file_path)
                start = self.route_copier.start()
                if not start:
                    messagebox.showerror("Error when starting the route copier! Please report any errors in your console to the github")
            else:
                messagebox.showerror("Route file path is not set! Please browse for a route file")
        else:
            messagebox.showerror("Journal file path is not set! Please browse for your latest log file")


root = tk.Tk()
ui = UI(root)
ui.create_widgets()
root.mainloop()
