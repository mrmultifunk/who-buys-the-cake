import tkinter as tk
from tkinter import messagebox

class CakeBuyerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cake Buyer Calculator")

        self.data = {}  # This will store the name and amount spent by each person

        # UI Elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Amount Paid ($):").grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Add/Update Payment", command=self.update_payment)
        self.add_button.grid(row=2, column=0, columnspan=2)

        self.result_label = tk.Label(self.root, text="", font=('Helvetica', 16))
        self.result_label.pack(pady=10)

        self.calculate_button = tk.Button(self.root, text="Who Buys the Cake?", command=self.calculate_next_buyer)
        self.calculate_button.pack()

    def update_payment(self):
        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()
        if name and amount.isdigit():
            self.data[name] = self.data.get(name, 0) + int(amount)
            messagebox.showinfo("Update Successful", f"Updated payments: {name} has paid ${self.data[name]}")
        else:
            messagebox.showerror("Error", "Please enter a valid name and amount.")
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def calculate_next_buyer(self):
        if not self.data:
            messagebox.showinfo("Info", "No data available.")
            return
        # Determine who has paid the least
        min_payment = min(self.data.values())
        potential_buyers = [name for name, amount in self.data.items() if amount == min_payment]
        buyers = ", ".join(potential_buyers)
        self.result_label.config(text=f"{buyers} should buy the next cake.")

# Set up the root window
root = tk.Tk()
app = CakeBuyerApp(root)
root.mainloop()
