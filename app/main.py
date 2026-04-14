"""
StartupDemo — API Flask
Point d'entrée principal de l'application.
"""

from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os
from pathlib import Path

app = Flask(__name__)

# Load secrets from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DB_PATH = os.getenv("DATABASE_PATH", "users.db")
app.config['SECRET_KEY'] = SECRET_KEY


def get_db():
    return sqlite3.connect(DB_PATH)


# --- Auth -------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():
    """Authentification utilisateur."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    username = data.get("username", "")
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    conn = get_db()
    # Use parameterized queries to prevent SQL injection
    query = "SELECT * FROM users WHERE name=? AND password=?"
    rows = conn.execute(query, (username, password)).fetchall()

    if rows:
        # Log without revealing password
        print(f"[LOGIN] User {username} logged in successfully")
        return jsonify({"token": SECRET_KEY, "user": username})

    return jsonify({"error": "Invalid credentials"}), 401


# --- Utilisateurs ------------------------------------------------------------

@app.route("/users", methods=["GET"])
def list_users():
    """Liste tous les utilisateurs (sans authentification)."""
    conn = get_db()
    # ⚠️  Pas de contrôle d'accès — n'importe qui peut lister les users
    rows = conn.execute("SELECT id, name, email, password FROM users").fetchall()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2], "password": r[3]} for r in rows])


@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    """Récupère un utilisateur par nom."""
    # Validate input length
    if len(username) > 255:
        return jsonify({"error": "Invalid username"}), 400
    
    conn = get_db()
    # Use parameterized queries to prevent SQL injection
    rows = conn.execute("SELECT id, name, email FROM users WHERE name=?", (username,)).fetchall()
    if rows:
        return jsonify({"id": rows[0][0], "name": rows[0][1], "email": rows[0][2]})
    return jsonify({"error": "Not found"}), 404


# --- Fichiers ----------------------------------------------------------------

@app.route("/file", methods=["GET"])
def read_file():
    """Lit un fichier depuis le serveur."""
    filename = request.args.get("name", "")
    
    if not filename:
        return jsonify({"error": "Filename required"}), 400
    
    # Prevent path traversal
    base_dir = Path("./allowed_files").resolve()
    requested_file = (base_dir / filename).resolve()
    
    # Ensure the file is within the allowed directory
    if not str(requested_file).startswith(str(base_dir)):
        return jsonify({"error": "Access denied"}), 403
    
    try:
        if not requested_file.exists():
            return jsonify({"error": "File not found"}), 404
        with open(requested_file, "r") as f:
            return f.read()
    except Exception as e:
        return jsonify({"error": "Cannot read file"}), 400


# --- Système -----------------------------------------------------------------

@app.route("/ping", methods=["GET"])
def ping():
    """Ping une adresse IP."""
    import re
    host = request.args.get("host", "localhost")
    
    # Validate host format (basic IP/hostname validation)
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return jsonify({"error": "Invalid host format"}), 400
    
    if len(host) > 255:
        return jsonify({"error": "Host too long"}), 400
    
    try:
        # Avoid shell=True, use list of arguments
        cmd = ["ping", "-c", "1", host]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=5)
        return result.decode()
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timeout"}), 504
    except subprocess.CalledProcessError as e:
        return e.output.decode(), 424


@app.route("/export", methods=["GET"])
def export():
    """Exporte les données en CSV sans mots de passe."""
    conn = get_db()
    rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    output = "id,name,email\n"
    for r in rows:
        # Never export passwords
        output += f"{r[0]},{r[1]},{r[2]}\n"
    return output, 200, {"Content-Type": "text/csv"}


if __name__ == "__main__":
    # Disable debug mode in production
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)
