# SecureSync Backup Software

SecureSync is a backup software that integrates with Google Drive, providing secure backup and restore functionalities with a user-friendly interface. It includes features such as Google authentication, local and cloud backups, scheduled backups, and a modern UI displaying space usage information.

## Features

- **Google Drive Integration**: Backup and restore files directly from Google Drive.
- **Local Backups**: Optionally compress and encrypt local backups.
- **Beautiful UI**: Displays space usage information and provides options to manage backups.
- **Scheduled Backups**: Automatically back up files at specified intervals.
- **Notifications**: Receive notifications for backup and restore operations.
- **File Management**: Download or delete backed-up files both from the cloud and locally.

## Installation

### Prerequisites

- Python 3.x
- Google Cloud project with Google Drive API enabled
- OAuth 2.0 credentials file

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/securesync.git
   cd securesync
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Setup Google Authentication**:
   - Create a Google Cloud project.
   - Enable the Google Drive API.
   - Download the OAuth 2.0 credentials file and place it in the `auth` directory as `credentials.json`.
   - The first time you run the application, you will be prompted to authenticate and authorize the application. This will generate a `token.json` file in the `auth` directory.

4. **Run the application**:
   ```sh
   python main.py
   ```

## Usage

1. **Launch the application**:
   ```sh
   python main.py
   ```

2. **Login**:
   - The application will prompt you to log in using your Google account.

3. **Backup**:
   - Navigate to the Backup tab.
   - Enter the source and destination directories.
   - Click "Backup Now" to back up your files.

4. **Restore**:
   - Navigate to the Restore tab.
   - View the list of backed-up files.
   - Select a file to download or delete.

5. **Settings**:
   - Navigate to the Settings tab.
   - Set the backup interval (in seconds) and schedule backups.

## Project Structure

```
secure_sync/
├── README.md
├── main.py
├── ui/
│   ├── __init__.py
│   └── ui.py
├── auth/
│   ├── __init__.py
│   └── google_auth.py
├── backup/
│   ├── __init__.py
│   └── backup_engine.py
├── scheduler/
│   ├── __init__.py
│   └── scheduler.py
├── cloud/
│   ├── __init__.py
│   └── google_drive.py
├── database/
│   ├── __init__.py
│   └── database.py
├── notifications/
│   ├── __init__.py
│   └── notifications.py
└── requirements.txt
```

## Modules

### UI Module (`ui/ui.py`)
Handles the graphical user interface using `tkinter` and `ttkbootstrap`.

### Authentication Module (`auth/google_auth.py`)
Handles Google authentication and token management.

### Backup Module (`backup/backup_engine.py`)
Manages file backup operations including optional compression and encryption.

### Scheduler Module (`scheduler/scheduler.py`)
Handles scheduling of backup tasks using the `schedule` library.

### Cloud Module (`cloud/google_drive.py`)
Handles interactions with Google Drive for uploading, downloading, and managing files.

### Database Module (`database/database.py`)
Manages metadata about backups using SQLite.

### Notifications Module (`notifications/notifications.py`)
Handles user notifications for backup and restore operations.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.
