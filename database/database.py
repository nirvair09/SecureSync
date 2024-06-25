import sqlite3

class Database:
    def __init__(self, db_name='backup.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS backups (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        file_name TEXT NOT NULL,
                                        file_id TEXT NOT NULL,
                                        user TEXT NOT NULL
                                      )''')

    def add_backup(self, file_name, file_id, user):
        with self.connection:
            self.connection.execute('INSERT INTO backups (file_name, file_id, user) VALUES (?, ?, ?)', 
                                    (file_name, file_id, user))

    def get_backups(self, user):
        with self.connection:
            cursor = self.connection.execute('SELECT file_name, file_id FROM backups WHERE user = ?', (user,))
            return cursor.fetchall()

    def delete_backup(self, file_id):
        with self.connection:
            self.connection.execute('DELETE FROM backups WHERE file_id = ?', (file_id,))
