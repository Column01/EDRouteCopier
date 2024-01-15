import csv
import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from ed_log_watcher import EDLogWatcher

PAD = {
    "padx": 5,
    "pady": 5
}
MINSIZE = (800, 400)


class UI:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("ED Route Copier")
        self.master.geometry("800x400")
        self.master.minsize(*MINSIZE)

        # Filled when Load route button is clicked
        self.journal_file_path = None
        self.route_file_path = None
        self.last_jump = False
        self.total_distance = 0
        self.total_jumps = 0
        self.estimated_jumps = 0
        self.route_copier = None

    def create_widgets(self) -> None:
        journal_frame = tk.Frame(self.master)
        journal_frame.pack(fill=tk.X)
        # Journal File Label
        self.label_journal = ttk.Label(journal_frame, text="Latest Journal: ", font=("Helvetica", 12, "bold", "underline"))
        self.label_journal.pack(side=tk.LEFT, **PAD)
        # Display for file path
        self.entry_journal = ttk.Entry(journal_frame, width=50, state="readonly")
        self.entry_journal.pack(side=tk.LEFT, fill=tk.X, **PAD)

        # Browse Button
        self.browse_journal_button = ttk.Button(journal_frame, text="Browse", command=self.browse_journal)
        self.browse_journal_button.pack(side=tk.LEFT, **PAD)

        route_frame = tk.Frame(self.master)
        route_frame.pack(fill=tk.X)
        # Route File Label
        self.label_route = ttk.Label(route_frame, text="Neutron Route:", font=("Helvetica", 12, "bold", "underline"))
        self.label_route.pack(side=tk.LEFT, **PAD)
        # Display for file path
        self.entry_route = ttk.Entry(route_frame, width=50, state="readonly")
        self.entry_route.pack(side=tk.LEFT, fill=tk.X, **PAD)
        # Browse Button
        self.browse_route_button = ttk.Button(route_frame, text="Browse", command=self.browse_route)
        self.browse_route_button.pack(side=tk.LEFT, **PAD)

        # Pilot status
        status_frame = tk.Frame(self.master)
        status_frame.pack(fill=tk.X)
        self.cur_system_label = ttk.Label(status_frame, text="Current System: Unknown")
        self.cur_system_label.pack(side=tk.LEFT, **PAD)

        self.target_system_label = ttk.Label(status_frame, text="Target System: None")
        self.target_system_label.pack(side=tk.LEFT, **PAD)

        self.route_target_label = ttk.Label(status_frame, text="Next Route Target: None")
        self.route_target_label.pack(side=tk.LEFT, **PAD)

        metrics_frame = tk.Frame(self.master)
        metrics_frame.pack(fill=tk.X)
        self.jumps_remaining_label = ttk.Label(metrics_frame, text="Jumps Remaining: 0")
        self.jumps_remaining_label.pack(side=tk.LEFT, **PAD)

        self.total_jumps_label = ttk.Label(metrics_frame, text="Jumps Made/Total: 0/Unknown")
        self.total_jumps_label.pack(side=tk.LEFT, **PAD)

        self.dist_traveled_label = ttk.Label(metrics_frame, text="Distance Traveled: 0ly")
        self.dist_traveled_label.pack(side=tk.LEFT, **PAD)

        text_frame = tk.Frame(self.master)
        text_frame.pack(fill=tk.BOTH, expand=True, **PAD)
        # Text box for info from the route copier code
        self.info_box = scrolledtext.ScrolledText(text_frame, height=13, state="disabled", **PAD)
        self.info_box.pack(side=tk.TOP, fill=tk.BOTH)

        button_frame = tk.Frame(self.master)
        button_frame.pack(fill=tk.X)
        # Load route button
        self.button = ttk.Button(button_frame, text="Load Route", command=self.load_route)
        self.button.pack(side=tk.LEFT, **PAD)

    def _nav_generator(self, verbose=True) -> dict:
        if verbose:
            self.write_text(f"Loading neutron route from file: {self.route_file_path}")
        with open(self.route_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def browse_journal(self) -> None:
        path = self.get_journal_path()
        self.journal_file_path = filedialog.askopenfilename(title="Journal File", initialdir=path, filetypes=[("Journal Files", ".log")])
        if self.journal_file_path:
            self.populate_entry(self.entry_journal, self.journal_file_path)

    def browse_route(self) -> None:
        self.route_file_path = filedialog.askopenfilename(title="Route File", initialdir="/", filetypes=[("Route Files", ".csv")])
        if self.route_file_path:
            self.populate_entry(self.entry_route, self.route_file_path)

    def populate_entry(self, entry: ttk.Entry, text: str) -> None:
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.configure(state="readonly")
    
    def update_label(self, label: ttk.Label, text: str) -> None:
        label.configure(text=text)
        label.update()

    def write_text(self, text: str, clear=False) -> None:
        self.info_box.configure(state="normal")
        if clear:
            self.info_box.delete(1.0, tk.END)
        else:
            self.info_box.insert(tk.INSERT, text + "\n")
        self.info_box.configure(state="disabled")
    
    def copy_to_clip(self, text: str) -> None:
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.master.update()

    def get_journal_path(self) -> str:
        _platform = platform.system()
        if _platform == "Windows":
            user = os.environ.get("USERNAME")
            path = os.path.join("C:\\Users", user, "Saved Games\\Frontier Developments\\Elite Dangerous")
            if os.path.isdir(path):
                return path
        return "/"
    
    def get_estimated_jumps(self) -> int:
        return sum(int(target["Jumps"]) for target in self._nav_generator(verbose=False))

    def on_journal(self, json_data: dict) -> None:
        event = json_data.get("event")
        # CMDR has FSD Jumped to a system
        if event == "FSDJump":
            # Get the system we entered
            star_system = json_data.get("StarSystem")

            # Metrics
            distance_jumped = json_data.get("JumpDist")
            self.total_distance += distance_jumped
            self.total_jumps += 1
            self.update_label(self.dist_traveled_label, f"Distance Traveled: {self.total_distance:.2f}ly")
            self.update_label(self.total_jumps_label, f"Jumps Made/Total: {self.total_jumps}/{self.estimated_jumps}")

            # Log the jump
            self.write_text(f"You have arrived in {star_system}")
            self.update_label(self.cur_system_label, f"Current System: {star_system}")
            # Check if the system is the one we were targetting, if it is, copy the next system to the clipboard
            if star_system == self.nav_target["System Name"]:
                try:
                    self.nav_target = next(self.nav)
                    new_target = self.nav_target["System Name"]
                    if new_target:
                        self.copy_to_clip(new_target)
                        self.write_text(f"You have reached the target system! Copied next system: {new_target}")
                        self.update_label(self.route_target_label, f"Next Route Target: {new_target}")
                    else:
                        self.write_text("Couldn't copy next system in route! See console for details")
                except StopIteration:
                    self.write_text("Reached the end of the route! Congratulations, CMDR, and good luck! o7")
                    self.update_label(self.route_target_label, "Next Route Target: None")
            
            # Hack to set last jump to zero properly
            if self.last_jump:
                self.update_label(self.jumps_remaining_label, f"Jumps Remaining: 0")
                self.last_jump = False

        elif event == "FSDTarget":
            # Player set their nav target in the galaxy map
            jumps_remaining = json_data.get("RemainingJumpsInRoute")
            target_system = json_data.get("Name")
            if jumps_remaining == 1:
                self.last_jump = True
            self.update_label(self.jumps_remaining_label, f"Jumps Remaining: {jumps_remaining}")
            self.update_label(self.target_system_label, f"Target System: {target_system}")

        elif event == "Shutdown":
            # Player shut the game down
            self.update_label(self.cur_system_label, "Current System: Unknown")
            self.update_label(self.route_target_label, "Next Route Target: None")
            self.update_label(self.jumps_remaining_label, f"Jumps Remaining: 0")
            self.update_label(self.target_system_label, f"Target System: None")
            self.write_text("Game has been shut down")
        
        elif event == "Location":
            # Game has started, load some info
            star_system = json_data.get("StarSystem")
            self.update_label(self.cur_system_label, f"Current System: {star_system}")
        
    def reset_metrics(self) -> None:
        self.total_distance = 0
        self.total_jumps = 0
        self.estimated_jumps = 0

    def load_route(self) -> None:
        if self.journal_file_path:
            if self.route_file_path:
                # Initialize the log watcher and listen for all journal events
                self.log_watcher = EDLogWatcher(self.journal_file_path, self.route_file_path)
                start = self.log_watcher.start()
                self.log_watcher.register_callback("all", self.on_journal)
                # Turn the neutron route into a generator object and get the first target
                self.nav = self._nav_generator()
                self.nav_target = next(self.nav)
                # Reset the metrics, gather the estimated jumps required and update the label
                self.reset_metrics()
                self.estimated_jumps = self.get_estimated_jumps()
                self.update_label(self.total_jumps_label, f"Jumps Made/Total: {self.total_jumps}/{self.estimated_jumps}")
                # Clear the info box so we know whats going on
                self.write_text("", clear=True)
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
