import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import json
import os
import shutil

class CakeRotationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cake Payment Manager")
        self.master.geometry('800x750')

        self.members = {}
        self.history = []
        self.current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.data_file = "team_data.json"
        self.current_payer_index = 0
        
        if not os.path.exists(self.data_file):
            self.save_data()
        self.load_data()
        self.setup_ui()
        self.select_next_payer()

    def setup_ui(self):
        self.frame = ttk.Frame(self.master)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.frame, text="Cake Payment Manager", font=('Helvetica', 16)).grid(row=0, columnspan=5)

        self.member_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.member_listbox.grid(row=1, column=0, columnspan=2, pady=5)
        self.update_member_listbox()

        self.add_edit_button = ttk.Button(self.frame, text="Add/Edit Member", command=self.add_or_edit_member)
        self.add_edit_button.grid(row=2, column=0, pady=5)

        self.absent_button = ttk.Button(self.frame, text="Toggle Absence", command=self.toggle_absence)
        self.absent_button.grid(row=2, column=1, pady=5)

        self.reset_button = ttk.Button(self.frame, text="Reset Statistics", command=self.reset_statistics)
        self.reset_button.grid(row=3, column=0, pady=5)

        self.pay_button = ttk.Button(self.frame, text="Record Payment", command=self.record_payment)
        self.pay_button.grid(row=3, column=1, pady=5)

        self.stats_tree = ttk.Treeview(self.frame, columns=('Member', 'Paid', 'Times', 'Last Payment', 'Absent', 'Absence Count'), show='headings', height=10)
        self.stats_tree.grid(row=4, column=0, columnspan=5, pady=10)
        self.stats_tree.heading('Member', text='Member')
        self.stats_tree.heading('Paid', text='Total Paid')
        self.stats_tree.heading('Times', text='Times Paid')
        self.stats_tree.heading('Last Payment', text='Last Payment Date')
        self.stats_tree.heading('Absent', text='Absent')
        self.stats_tree.heading('Absence Count', text='Absence Count')
        self.stats_tree.column('Member', width=120)
        self.stats_tree.column('Paid', width=100)
        self.stats_tree.column('Times', width=100)
        self.stats_tree.column('Last Payment', width=150)
        self.stats_tree.column('Absent', width=80)
        self.stats_tree.column('Absence Count', width=120)
        self.update_stats_tree()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.members = data.get('members', {})
                self.history = data.get('history', {})
                self.current_payer_index = data.get('current_payer_index', 0)

    def save_data(self):
        data = {
            'members': self.members,
            'history': self.history,
            'current_payer_index': self.current_payer_index
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def update_member_listbox(self):
        self.member_listbox.delete(0, tk.END)
        for i, (member, details) in enumerate(self.members.items()):
            status = "Absent" if details.get('is_absent', False) else "Present"
            entry = f"{member} - {status}"
            self.member_listbox.insert(tk.END, entry)
            if i == self.current_payer_index:
                self.member_listbox.itemconfig(i, {'bg': 'lightgreen'})  

    def add_or_edit_member(self):
        name = simpledialog.askstring("Member Name", "Enter the member's name:")
        if name:
            if name not in self.members:
                self.members[name] = {'total_paid': 0, 'times_paid': 0, 'is_absent': False, 'last_payment_date': None, 'absence_count': 0}
            self.save_data()
            self.update_member_listbox()
            self.update_stats_tree()

    def toggle_absence(self):
        selected = self.member_listbox.curselection()
        if selected:
            member = list(self.members.keys())[selected[0]]
            self.members[member]['is_absent'] = not self.members[member].get('is_absent', False)
            if self.members[member]['is_absent']:
                self.members[member]['absence_count'] += 1
            else:
                self.members[member]['absence_count'] -= 1
            if selected[0] == self.current_payer_index:  # If the currently selected payer is marked as absent
                self.select_next_payer()  # Select the next non-absent member
            self.save_data()
            self.update_member_listbox()

    def reset_statistics(self):
        if messagebox.askyesno("Reset Statistics", "Are you sure you want to reset all statistics?"):
            backup_file = self.data_file.replace('.json', '_backup.json')
            shutil.copy(self.data_file, backup_file)
            for member in self.members:
                self.members[member]['total_paid'] = 0
                self.members[member]['times_paid'] = 0
                self.members[member]['last_payment_date'] = None
                self.members[member]['absence_count'] = 0
            self.history.clear()
            self.save_data()
            self.update_stats_tree()
            messagebox.showinfo("Reset Complete", "All statistics have been reset. Backup saved as " + backup_file)

    def record_payment(self):
        if self.members:
            member = list(self.members.keys())[self.current_payer_index]
            amount = simpledialog.askinteger("Payment Amount", "Enter the amount paid:", initialvalue=60)
            if amount:
                self.members[member]['total_paid'] += amount
                self.members[member]['times_paid'] += 1
                self.members[member]['last_payment_date'] = self.current_date
                self.history.append({'date': self.current_date, 'member': member, 'amount': amount})
                self.save_data()
                self.update_stats_tree()
                messagebox.showinfo("Payment Recorded", f"{member} has paid {amount} DKK.")
                self.select_next_payer()

    def update_stats_tree(self):
        self.stats_tree.delete(*self.stats_tree.get_children())
        for member, details in self.members.items():
            status = "Absent" if details.get('is_absent', False) else "Present"
            last_payment_date = details['last_payment_date'] if details['last_payment_date'] else "Never"
            self.stats_tree.insert('', 'end', values=(member, details['total_paid'], details['times_paid'], last_payment_date, status, details['absence_count']))

    def select_next_payer(self):
        if self.members:
            absent_members = [member for member, details in self.members.items() if not details.get('is_absent', False)]
            if len(absent_members) == 0:  # If all members are absent
                self.current_payer_index = 0
            else:
                self.current_payer_index = (self.current_payer_index + 1) % len(self.members)
                while self.members[list(self.members.keys())[self.current_payer_index]].get('is_absent', False):
                    self.current_payer_index = (self.current_payer_index + 1) % len(self.members)
            self.update_member_listbox()

root = tk.Tk()
app = CakeRotationApp(root)
root.mainloop()
