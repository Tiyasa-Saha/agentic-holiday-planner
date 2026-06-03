import sqlite3
from datetime import datetime


class SQLiteMemory:
    def __init__(self, db_path="memory/user_preferences.db"):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, preference_key)
            )
        """)

        conn.commit()
        conn.close()

    def save_preference(self, user_id: str, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences
            (user_id, preference_key, preference_value, updated_at)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            key,
            value,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def get_all_preferences(self, user_id: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT preference_key, preference_value
            FROM user_preferences
            WHERE user_id = ?
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        return dict(rows)

    def delete_preference(self, user_id: str, key: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM user_preferences
            WHERE user_id = ? AND preference_key = ?
        """, (user_id, key))

        conn.commit()
        conn.close()

    def clear_preferences(self, user_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM user_preferences
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def format_preferences_for_agent(self, user_id: str) -> str:
        preferences = self.get_all_preferences(user_id)

        if not preferences:
            return "No saved preferences for this user."

        lines = []

        for key, value in preferences.items():
            lines.append(f"- {key}: {value}")

        return "\n".join(lines)