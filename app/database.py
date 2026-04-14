"""
Initialisation de la base de données.
Script à lancer une seule fois pour créer les tables et données de test.
"""

import sqlite3
import os
try:
    import bcrypt
except ImportError:
    import hashlib
    bcrypt = None

DB_PATH = os.getenv("DATABASE_PATH", "users.db")

# Use environment variables for sensitive credentials
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
SENDGRID_TOKEN = os.getenv("SENDGRID_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")


def hash_password(password):
    """Hash password using bcrypt for secure storage."""
    if bcrypt:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    else:
        # Fallback to PBKDF2 if bcrypt not available
        import hashlib
        return hashlib.pbkdf2_hmac('sha256', password.encode(), os.urandom(32), 100000).hex()


def verify_password(password, hashed):
    """Verify password against hash."""
    if bcrypt:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    else:
        return hash_password(password) == hashed


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
