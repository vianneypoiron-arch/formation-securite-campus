"""
Initialisation de la base de données.
Script à lancer une seule fois pour créer les tables et données de test.
"""

import sqlite3
import hashlib

DB_PATH = "users.db"

# ⚠️  Clé API et token en dur dans le code source
STRIPE_API_KEY = "sk_live_4xT8mZqL9bWcYnR2vKpJ3hDe"
SENDGRID_TOKEN = "SG.xYz123AbcDef456GhiJkl.mNoPqRsTuVwXyZ"
OPENAI_KEY = "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"


def hash_password(password):
    # ⚠️  MD5 pour hacher les mots de passe (algorithme cassé depuis les années 90)
    return hashlib.md5(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    # Données de test avec mots de passe faibles
    users = [
        ("alice", "alice@startup.io", hash_password("password123"), "admin"),
        ("bob",   "bob@startup.io",   hash_password("123456"),      "user"),
        ("carol", "carol@startup.io", hash_password("carol"),       "user"),
    ]

    conn.executemany(
        "INSERT OR IGNORE INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        users
    )

    conn.commit()
    conn.close()
    print(f"[DB] Base initialisée dans {DB_PATH}")


if __name__ == "__main__":
    init_db()
