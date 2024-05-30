import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_info_cfg(self, user_id, api_id, api_hash, text, phone):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, api_id, api_hash, text, phone) VALUES (?, ?, ?, ?, ?)", (user_id, api_id, api_hash, text, phone,))

    def add_code(self, user_id, code):
        with self.connection:
            self.cursor.execute("UPDATE users SET code = ? WHERE user_id = ?", (code, user_id,))

    def add_chat(self, user_id, name):
        with self.connection:
            self.cursor.execute("INSERT INTO chats (user_id, name) VALUES (?, ?)", (user_id, name,))


class SpamerDB(Database):
    def __init__(self, db_file):
        super().__init__(db_file)

    def get_hash(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT api_hash FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return str(res[0])

    def get_api_id(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT api_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(res[0])

    def get_all_names(self, user_id):
        with self.connection:
            # Execute the SQL query to get all names for the given user_id
            result = self.cursor.execute("SELECT name FROM chats WHERE user_id = ?", (user_id,)).fetchall()

            # Extract the names from the result
            names = [row[0] for row in result]
            print(names)

            # Return the list of names
            return names

    def get_text(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT text FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return str(res[0])

    def get_phone_number(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT phone FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return str(res[0])

    def get_code(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT code FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return str(res[0])

    def get_sec(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT sec FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(res[0])

    def get_time(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT time FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(res[0])

    def get_status_script(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT start FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(res[0])

    def get_photo_path(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT photo FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return str(res[0]) if res and res[0] else None

    def delete_info(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))