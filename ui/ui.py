import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from backup.backup_engine import BackupEngine
from scheduler.scheduler import Scheduler
from cloud.google_drive import GoogleDrive
from auth.google_auth import GoogleAuth
from database.database import Database
from notifications.notifications import Notifications
import os

class SecureSyncUI:
    def __init__(self, master):
        self.master = master
        self.master.title("SecureSync Backup Software")
        self.master.geometry("600x400")
        
        self.notebook = ttk.Notebook(self.master)
        self.backup_frame = ttk.Frame(self.notebook)
        self.restore_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.backup_frame, text='Backup')
        self.notebook.add(self.restore_frame, text='Restore')
        self.notebook.add(self.settings_frame, text='Settings')
        self.notebook.pack(expand=1, fill='both')

        self.auth = GoogleAuth('path/to/credentials.json', 'path/to/token.json')
        self.creds = self.auth.login()
        self.drive = GoogleDrive(self.creds)
        self.db = Database()
        self.notifications = Notifications()
        self.scheduler = Scheduler()
        self.backup_engine = BackupEngine()

        self.create_backup_tab()
        self.create_restore_tab()
        self.create_settings_tab()
        self.update_space_info()

    def create_backup_tab(self):
        ttk.Label(self.backup_frame, text="Source Directory:").grid(row=0, column=0, padx=10, pady=10)
        self.source_entry = ttk.Entry(self.backup_frame)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.backup_frame, text="Destination Directory:").grid(row=1, column=0, padx=10, pady=10)
        self.dest_entry = ttk.Entry(self.backup_frame)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10)

        backup_button = ttk.Button(self.backup_frame, text="Backup Now", command=self.backup_now)
        backup_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.space_frame = ttk.LabelFrame(self.backup_frame, text="Space Info")
        self.space_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.space_used_label = ttk.Label(self.space_frame, text="Used Space: 0 GB")
        self.space_used_label.grid(row=0, column=0, padx=10, pady=5)
        self.space_remaining_label = ttk.Label(self.space_frame, text="Remaining Space: 15 GB")
        self.space_remaining_label.grid(row=0, column=1, padx=10, pady=5)

    def backup_now(self):
        source = self.source_entry.get()
        destination = self.dest_entry.get()
        self.backup_engine.backup_files(source, destination)
        file_id = self.drive.upload_file(destination)
        self.db.add_backup(os.path.basename(destination), file_id, "user")  # Replace "user" with actual user identification
        self.notifications.notify("Backup completed successfully.")
        self.update_space_info()

    def create_restore_tab(self):
        self.file_listbox = tk.Listbox(self.restore_frame)
        self.file_listbox.pack(expand=1, fill='both', padx=10, pady=10)
        
        refresh_button = ttk.Button(self.restore_frame, text="Refresh", command=self.refresh_file_list)
        refresh_button.pack(pady=10)

        delete_button = ttk.Button(self.restore_frame, text="Delete", command=self.delete_file)
        delete_button.pack(pady=10)

        download_button = ttk.Button(self.restore_frame, text="Download", command=self.download_file)
        download_button.pack(pady=10)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        backups = self.db.get_backups("user")  # Replace "user" with actual user identification
        for backup in backups:
            self.file_listbox.insert(tk.END, f"{backup[0]} (ID: {backup[1]})")

    def delete_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            file_id = selected_file.split("ID: ")[1].strip(")")
            self.drive.delete_file(file_id)
            self.db.delete_backup(file_id)
            self.refresh_file_list()
            self.notifications.notify("File deleted successfully.")
            self.update_space_info()

    def download_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            file_id = selected_file.split("ID: ")[1].strip(")")
            dest_path = tk.filedialog.askdirectory()
            self.drive.download_file(file_id, dest_path)
            self.notifications.notify(f"File downloaded to {dest_path}")

    def create_settings_tab(self):
        ttk.Label(self.settings_frame, text="Backup Interval (in seconds):").grid(row=0, column=0, padx=10, pady=10)
        self.interval_entry = ttk.Entry(self.settings_frame)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)

        schedule_button = ttk.Button(self.settings_frame, text="Schedule Backup", command=self.schedule_backup)
        schedule_button.grid(row=1, column=0, columnspan=2, pady=10)

    def schedule_backup(self):
        interval = int(self.interval_entry.get())
        self.scheduler.schedule_backup(interval, self.backup_now)
        self.notifications.notify("Backup scheduled successfully.")
        self.scheduler.start()

    def update_space_info(self):
        used, total = self.drive.get_storage_info()
        self.space_used_label.config(text=f"Used Space: {used:.2f} GB")
        self.space_remaining_label.config(text=f"Remaining Space: {total - used:.2f} GB")

def main():
    app = ttkb.Window(themename="superhero")
    SecureSyncUI(app)
    app.mainloop()

if __name__ == "__main__":
    main()
