import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import datetime
import json
import os
import shutil
import threading
from babel import Locale

def setup_styles():
    style = ttk.Style()
    style.theme_use('default')  # This sets the default theme which is usually more modern than 'clam' or 'classic'

    # General style configurations for a modern look
    style.configure('TFrame', background='white')
    style.configure('TButton', font=('Segoe UI', 10), borderwidth=1, relief='flat', background='white')
    style.configure('TLabel', font=('Segoe UI', 10), background='white', foreground='black')
    style.configure('TEntry', font=('Segoe UI', 10), borderwidth=1, relief='flat')
    style.configure('Treeview', font=('Segoe UI', 10), rowheight=25, borderwidth=0, background='white', relief='flat')
    style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'), background='white', foreground='black')

    # Button hover effects
    style.map('TButton', 
              background=[('active', '#E1E1E1'), ('pressed', '#D3D3D3'), ('!disabled', 'white')],
              foreground=[('active', 'black'), ('pressed', '#333333')])
    style.map('Treeview', background=[('selected', '#0078D7')], foreground=[('selected', 'white')])

class CakeRotationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cake Payment Manager")
        self.master.geometry('800x750')
        self.master.configure(bg='white')
        
        setup_styles()  # Apply the modern styles

        # Supported languages
        self.languages = {'en': 'English', 'de': 'German', 'da': 'Danish'}
        self.current_language = 'en'
        self.load_language()

        # Data structures to store member and payment history
        self.members = {}
        self.history = []
        self.current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.data_file = "team_data.json"

        # Main UI Frame setup
        self.ui_frame = ttk.Frame(self.master)
        self.ui_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Buttons for import and export actions
        self.import_backup_button = ttk.Button(self.ui_frame, text="Import Backup", command=self.import_backup)
        self.import_backup_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.export_data_button = ttk.Button(self.ui_frame, text="Export Data", command=self.export_data)
        self.export_data_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Initialize the user interface components
        self.setup_ui()

        # Load data and update UI
        self.load_data()

    def load_language(self):
        # Load language settings from file
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.current_language = settings.get('language', 'en')

    def save_language(self):
        # Save current language setting to file
        settings = {'language': self.current_language}
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def setup_ui(self):
        # Setup UI components within the main window
        self.frame = ttk.Frame(self.master)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        

        # Buttons for adding/editing members, toggling absence, resetting statistics, and recording payments
        self.add_edit_button = ttk.Button(self.frame, text=self.translate("Add/Edit Member"), command=self.add_or_edit_member)
        self.add_edit_button.grid(row=2, column=0, pady=5)
        self.absent_button = ttk.Button(self.frame, text=self.translate("Toggle Absence"), command=self.toggle_absence)
        self.absent_button.grid(row=2, column=1, pady=5)
        self.reset_button = ttk.Button(self.frame, text=self.translate("Reset Statistics"), command=self.reset_statistics)
        self.reset_button.grid(row=3, column=0, pady=5)
        self.pay_button = ttk.Button(self.frame, text=self.translate("Record Payment"), command=self.record_payment)
        self.pay_button.grid(row=3, column=1, pady=5)

        
        # Button for deleting a member
        self.delete_member_button = ttk.Button(self.frame, text=self.translate("Delete Member"), command=self.delete_member)
        self.delete_member_button.grid(row=3, column=2, pady=5)

        # Treeview for showing statistics
        self.stats_tree = ttk.Treeview(self.frame, columns=('Member', 'Paid', 'Times', 'Last Payment', 'Absent', 'Absence Count'), show='headings', height=10)
        self.stats_tree.grid(row=4, column=0, columnspan=5, pady=10)
        columns = ['Member', 'Paid', 'Times', 'Last Payment', 'Absent', 'Absence Count']
        translated_columns = [self.translate(col) for col in columns]
        for col, translated_col in zip(columns, translated_columns):
            self.stats_tree.heading(col, text=translated_col)
            self.stats_tree.column(col, width=120)
        self.update_stats_tree()

        # Button to open settings window
        self.settings_button = ttk.Button(self.frame, text=self.translate("Settings"), command=self.open_settings)
        self.settings_button.grid(row=5, column=0, columnspan=2, pady=5)

    def translate(self, text):
        # Column-specific translations
        column_translations = {
            'en': {
                'Member': 'Member',
                'Paid': 'Paid',
                'Times': 'Times',
                'Last Payment': 'Last Payment',
                'Absent': 'Absent',
                'Absence Count': 'Absence Count'
            },
            'de': {
                'Member': 'Mitglied',
                'Paid': 'Bezahlt',
                'Times': 'Mal',
                'Last Payment': 'Letzte Zahlung',
                'Absent': 'Abwesend',
                'Absence Count': 'Fehlzeiten'
            },
            'da': {
                'Member': 'Medlem',
                'Paid': 'Betalt',
                'Times': 'Gange',
                'Last Payment': 'Sidste Betaling',
                'Absent': 'Fraværende',
                'Absence Count': 'Fraværsantal'
            }
        }
        if text in column_translations.get(self.current_language, {}):
            return column_translations[self.current_language][text]
        # Translate text to the current language
        translations = {
            'en': {
                'Cake Payment Manager': 'Cake Payment Manager',
                'Add/Edit Member': 'Add/Edit Member',
                'Toggle Absence': 'Toggle Absence',
                
                'Delete Member': 'Delete Member',
                'Are you sure you want to delete {member}?': 'Are you sure you want to delete {member}?',
                'Record Payment': 'Record Payment',
                'Settings': 'Settings',
                'Language': 'Language',
                'Save': 'Save',
                'Absent': 'Absent',
                'Present': 'Present',
                'Never': 'Never',
                'Member Name': 'Member Name',
                'Enter the member\'s name:': 'Enter the member\'s name:',
                'Payment Amount': 'Payment Amount',
                'Enter the amount paid:': 'Enter the amount paid:',
                'has paid': 'has paid',
                'Reset Complete': 'Reset Complete',
                'All statistics have been reset.': 'All statistics have been reset.',
                'Are you sure you want to reset all statistics?': 'Are you sure you want to reset all statistics?'
            },
            'de': {
                'Cake Payment Manager': 'Kuchen Zahlungsmanager',
                'Add/Edit Member': 'Mitglied hinzufügen/bearbeiten',
                'Toggle Absence': 'Abwesenheit umschalten',
                
                'Delete Member': 'Mitglied löschen',
                'Are you sure you want to delete {member}?': 'Sind Sie sicher, dass Sie {member} löschen möchten?',
                'Record Payment': 'Zahlung aufzeichnen',
                'Settings': 'Einstellungen',
                'Language': 'Sprache',
                'Save': 'Speichern',
                'Absent': 'Abwesend',
                'Present': 'Anwesend',
                'Never': 'Nie',
                'Member Name': 'Mitgliedsname',
                'Enter the member\'s name:': 'Geben Sie den Namen des Mitglieds ein:',
                'Payment Amount': 'Zahlungsbetrag',
                'Enter the amount paid:': 'Geben Sie den gezahlten Betrag ein:',
                'has paid': 'hat bezahlt',
                'Reset Complete': 'Zurücksetzen abgeschlossen',
                'All statistics have been reset.': 'Alle Statistiken wurden zurückgesetzt.',
                'Are you sure you want to reset all statistics?': 'Sind Sie sicher, dass Sie alle Statistiken zurücksetzen möchten?'
            },
            'da': {
                'Cake Payment Manager': 'Kage Betalingsstyring',
                'Add/Edit Member': 'Tilføj/rediger medlem',
                'Toggle Absence': 'Skift fravær',
                
                'Delete Member': 'Slet medlem',
                'Are you sure you want to delete {member}?': 'Er du sikker på, at du vil slette {member}?',
                'Record Payment': 'Registrer betaling',
                'Settings': 'Indstillinger',
                'Language': 'Sprog',
                'Save': 'Gem',
                'Absent': 'Fraværende',
                'Present': 'Tilstede',
                'Never': 'Aldrig',
                'Member Name': 'Medlemsnavn',
                'Enter the member\'s name:': 'Indtast medlemmets navn:',
                'Payment Amount': 'Betalingsbeløb',
                'Enter the amount paid:': 'Indtast det betalte beløb:',
                'has paid': 'har betalt',
                'Reset Complete': 'Nulstilling fuldført',
                'All statistics have been reset.': 'Alle statistikker er blevet nulstillet.',
                'Are you sure you want to reset all statistics?': 'Er du sikker på, at du vil nulstille alle statistikker?'
            }
        }
        return translations.get(self.current_language, {}).get(text, text)
    
    def import_backup(self):
        # Ask the user to select a backup JSON file to import
        backup_file_path = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=(("JSON files", "*.json"),),
            defaultextension=".json"
        )
        
        if backup_file_path:
            # Ensure the selected file exists and read data from it
            if os.path.exists(backup_file_path):
                try:
                    with open(backup_file_path, 'r') as file:
                        backup_data = json.load(file)
                    
                    # Assuming backup_data contains similar structure to current data
                    if 'members' in backup_data and 'history' in backup_data:
                        self.members = backup_data['members']
                        self.history = backup_data['history']
                        
                        # Save loaded data to current data file for consistency
                        self.save_data()

                        # Update the UI to reflect the loaded data
                        self.update_member_listbox()
                        self.update_stats_tree()
                        messagebox.showinfo("Import Successful", "Backup data has been successfully imported.")
                    else:
                        messagebox.showerror("Import Error", "Invalid backup file format.")
                except json.JSONDecodeError as e:
                    messagebox.showerror("Import Error", f"Failed to import backup: {str(e)}")
            else:
                messagebox.showerror("File Error", "The selected file does not exist.")

    def load_data(self):
        """Load member and history data from the JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.members = data.get('members', {})
                    self.history = data.get('history', [])

                self.update_member_listbox()
                self.update_stats_tree()
            else:
                # If the file does not exist, create it with default data
                self.save_data()
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", "Failed to load data: " + str(e))
            # Create default data if JSON is corrupted or unreadable
            self.members = {}
            self.save_data()

    def save_data(self):
        """Save the current members and history to the JSON file."""
        data = {
            'members': self.members,
            'history': self.history
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def update_member_listbox(self):
        self.member_listbox.delete(0, tk.END)
        for i, (name, details) in enumerate(self.members.items()):
            status = "Absent" if details.get('is_absent', False) else "Present"
            entry = f"{name} - {status}"
            self.member_listbox.insert(tk.END, entry)
            if details.get('is_absent', False):
                self.member_listbox.itemconfig(i, {'bg': 'lightcoral'})
            else:
                self.member_listbox.itemconfig(i, {'bg': 'white'})

    def add_or_edit_member(self):
        # Add or edit a member's information
        name = simpledialog.askstring(self.translate("Member Name"), self.translate("Enter the member's name:"))
        if name:
            if name not in self.members:
                self.members[name] = {'total_paid': 0, 'times_paid': 0, 'is_absent': False, 'last_payment_date': None, 'absence_count': 0}
            self.save_data()
            self.update_member_listbox()
            self.update_stats_tree()

    

    def delete_member(self):
        # Delete a member's information
        selected = self.member_listbox.curselection()
        if selected:
            member_index = selected[0]
            member = list(self.members.keys())[member_index]
            if messagebox.askyesno(self.translate("Delete Member"), self.translate(f"Are you sure you want to delete {member}?")):
                del self.members[member]
                self.save_data()
                self.update_member_listbox()
                self.update_stats_tree()
                messagebox.showinfo(self.translate("Delete Member"), self.translate(f"{member} has been deleted."))

    def reset_statistics(self):
        # Reset all statistical data after confirmation
        if messagebox.askyesno(self.translate("Reset Statistics"), self.translate("Are you sure you want to reset all statistics?")):
            backup_file = f"team_data_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            shutil.copy(self.data_file, backup_file)
            for member in self.members:
                self.members[member] = {'total_paid': 0, 'times_paid': 0, 'is_absent': False, 'last_payment_date': None, 'absence_count': 0}
            self.history.clear()
            self.save_data()
            self.update_stats_tree()
            messagebox.showinfo(self.translate("Reset Complete"), self.translate("All statistics have been reset."))

    def record_payment(self):
        # Let the user select who is paying from the member list
        selected = self.member_listbox.curselection()
        if selected:
            member_index = selected[0]
            member = list(self.members.keys())[member_index]
            # Ask the user to enter the payment amount
            amount = simpledialog.askinteger(self.translate("Payment Amount"), self.translate("Enter the amount paid:"), initialvalue=50)
            if amount is not None:
                # Record the payment details
                self.members[member]['total_paid'] += amount
                self.members[member]['times_paid'] += 1
                self.members[member]['last_payment_date'] = self.current_date
                self.history.append({'date': self.current_date, 'member': member, 'amount': amount})
                self.save_data()
                self.update_stats_tree()
                messagebox.showinfo(self.translate("Payment Recorded"), f"{member} {self.translate('has paid')} {amount} DKK.")
            else:
                messagebox.showinfo("No Payment", "No payment amount was entered.")
        else:
            messagebox.showerror("Payment Error", "No valid payer is currently selected.")

    def update_stats_tree(self):
        # Update the statistics treeview with current data
        for i in self.stats_tree.get_children():
            self.stats_tree.delete(i)
        for member, details in self.members.items():
            status = self.translate("Absent") if details.get('is_absent', False) else self.translate("Present")
            last_payment_date = details['last_payment_date'] if details['last_payment_date'] else self.translate("Never")
            self.stats_tree.insert('', 'end', values=(member, details['total_paid'], details['times_paid'], last_payment_date, status, details['absence_count']))

    def open_settings(self):
        # Open the settings window for language selection
        settings_window = tk.Toplevel(self.master)
        settings_window.title(self.translate("Settings"))
        settings_window.geometry('300x200')
        ttk.Label(settings_window, text=self.translate("Language")).grid(row=0, column=0)
        language_var = tk.StringVar()
        language_var.set(self.current_language)
        language_dropdown = ttk.Combobox(settings_window, textvariable=language_var, values=list(self.languages.keys()))
        language_dropdown.grid(row=0, column=1)
        ttk.Button(settings_window, text=self.translate("Save"), command=lambda: self.save_settings(language_var.get(), settings_window)).grid(row=1, column=0, columnspan=2, pady=10)

    def save_settings(self, language, settings_window):
        # Save the selected language and update the UI texts
        self.current_language = language
        self.save_language()
        self.refresh_ui_texts()
        settings_window.destroy()

    def refresh_ui_texts(self):
        # Refresh all UI elements to reflect the current language
        self.master.title(self.translate("Cake Payment Manager"))
        self.add_edit_button.config(text=self.translate("Add/Edit Member"))
        self.absent_button.config(text=self.translate("Toggle Absence"))
        self.reset_button.config(text=self.translate("Reset Statistics"))
        self.pay_button.config(text=self.translate("Record Payment"))
        self.settings_button.config(text=self.translate("Settings"))
        columns = ['Member', 'Paid', 'Times', 'Last Payment', 'Absent', 'Absence Count']
        for col in columns:
            self.stats_tree.heading(col, text=self.translate(col))

    def export_data(self):
        # Export the current data to a JSON file selected by the user
        export_file_path = filedialog.asksaveasfilename(
            title="Export Data",
            filetypes=(("JSON files", "*.json"),),
            defaultextension=".json"
        )
        if export_file_path:
            def save_data_in_background():
                with open(export_file_path, 'w') as file:
                    export_data = {
                        'members': self.members,
                        'history': self.history
                    }
                    json.dump(export_data, file, indent=4)
                messagebox.showinfo("Export Successful", f"Data exported successfully to {export_file_path}")

            threading.Thread(target=save_data_in_background).start()

root = tk.Tk()
app = CakeRotationApp(root)
root.mainloop()
