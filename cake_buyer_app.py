import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, filedialog, ttk
import tkinter.font as tkFont
import datetime
import os

class CakeRotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cake Rotation Scheduler")
        self.root.geometry('400x500')  # Set a fixed size for the window

        self.custom_font = tkFont.Font(family="Helvetica", size=12)  # Custom font for widgets

        self.names = ["Brian", "Ulrik", "Dorthe", "Ian", "Eik", "Jesper", "Martin", "Frank"]
        self.index = 0
        self.history = []
        self.history_file = 'cake_history.txt'
        self.current_date = datetime.datetime.now()
        self.last_date = None  # Store the last date of assignment
        self.absentees = []  # List to store absentees

        self.setup_ui()
        self.load_history()
        self.display_next_buyer()

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.info_label = ttk.Label(self.frame, text="To pay the cake this week:", font=self.custom_font)
        self.info_label.grid(column=1, row=1, pady=10)

        self.next_buyer_label = ttk.Label(self.frame, text="", font=self.custom_font, foreground='blue')
        self.next_buyer_label.grid(column=1, row=2, pady=10)

        self.absent_button = ttk.Button(self.frame, text="Mark Absent", command=self.mark_absent)
        self.absent_button.grid(column=1, row=3, pady=10)

        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.grid(column=1, row=4, pady=20)

        self.future_button = ttk.Button(self.buttons_frame, text="Show Next 4 Weeks", command=self.show_future_buyers)
        self.future_button.grid(column=1, row=1, padx=10)

        self.reset_button = ttk.Button(self.buttons_frame, text="Reset Statistics", command=self.reset_statistics)
        self.reset_button.grid(column=2, row=1, padx=10)

        self.export_button = ttk.Button(self.buttons_frame, text="Export History", command=self.export_history)
        self.export_button.grid(column=3, row=1, padx=10)

        self.history_label = ttk.Label(self.frame, text="Purchase History:", font=self.custom_font)
        self.history_label.grid(column=1, row=5, pady=10)

        self.history_text = scrolledtext.ScrolledText(self.frame, width=40, height=10, font=self.custom_font)
        self.history_text.grid(column=1, row=6, pady=10)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                lines = file.readlines()
                self.history = [line.strip() for line in lines]
                if self.history:
                    last_entry = self.history[-1]
                    self.last_date = datetime.datetime.strptime(last_entry.split(":")[0], '%d-%m-%Y')
        self.update_history_text()

    def save_history(self):
        with open(self.history_file, 'w') as file:
            for entry in self.history:
                file.write(f"{entry}\n")

    def export_history(self):
        export_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                   title="Save history as...")
        if export_file:
            with open(export_file, 'w') as file:
                for entry in self.history:
                    file.write(f"{entry}\n")
            messagebox.showinfo("Export Successful", f"History has been exported to {export_file}.")

    def display_next_buyer(self):
        while self.names[self.index] in self.absentees:
            self.index = (self.index + 1) % len(self.names)
        self.next_buyer_label.config(text=f"{self.names[self.index]}")
        self.record_purchase(self.names[self.index])  # Automatically record the purchase

    def mark_absent(self):
        self.absentees.append(self.names[self.index])
        self.index = (self.index + 1) % len(self.names)
        self.display_next_buyer()

    def reset_statistics(self):
        if messagebox.askyesno("Reset Statistics", "Are you sure you want to reset all statistics? This cannot be undone."):
            self.history = []
            self.index = 0
            self.absentees = []
            self.last_date = None
            self.update_history_text()
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            messagebox.showinfo("Reset Complete", "All statistics have been reset.")
            self.display_next_buyer()

    def record_purchase(self, buyer):
        today = datetime.datetime.now()
        formatted_date = today.strftime('%d-%m-%Y')
        entry = f"{formatted_date}: {buyer} paid 60 DKK"  # Default amount, could be configurable
        self.history.append(entry)
        self.save_history()
        self.update_history_text()
        self.index = (self.index + 1) % len(self.names)

    def show_future_buyers(self):
        future_dates = [datetime.datetime.now() + datetime.timedelta(weeks=i) for i in range(1, 5)]
        future_buyers = [(self.names[(self.index + i) % len(self.names)], date.strftime('%d-%m-%Y')) for i, date in enumerate(future_dates)]
        future_text = "\n".join(f"{date}: {buyer}" for buyer, date in future_buyers)
        messagebox.showinfo("Next 4 Weeks' Buyers", future_text)

    def update_history_text(self):
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + '\n')

root = tk.Tk()
app = CakeRotationApp(root)
root.mainloop()
