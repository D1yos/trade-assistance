import sqlite3
import hashlib


class Database:
    def __init__(self, db_name="rates.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.check_columns()

    def create_tables(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users
                            (
                                username TEXT PRIMARY KEY, password TEXT
                            )
                            """)
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS rates
                            (
                                item_from TEXT, item_to TEXT, amount_from REAL, amount_to REAL, PRIMARY KEY
                                (
                                    item_from, item_to
                                )
                            )
                            """)
        self.conn.commit()

    def check_columns(self):
        try:
            self.cursor.execute("PRAGMA table_info(rates)")
            columns = [column[1] for column in self.cursor.fetchall()]

            if columns and "amount_from" not in columns:
                print("Detected old schema. Resetting 'rates' table...")
                self.cursor.execute("DROP TABLE rates")
                self.create_tables()
        except Exception as e:
            print(f"Migration error: {e}")

    def register_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
        return self.cursor.fetchone() is not None

    def update_rate(self, f, t, n, x):
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO rates (item_from, item_to, amount_from, amount_to)
                VALUES (?, ?, ?, ?)
            """, (f, t, n, x))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating rate: {e}")

    def get_all_rates(self):
        self.cursor.execute("SELECT * FROM rates")
        return self.cursor.fetchall()

    def clear_all(self):
        self.cursor.execute("DELETE FROM rates")
        self.conn.commit()