"""
StartupDemo — API Flask
Point d'entrée principal de l'application.
"""

from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)

# ⚠️  Clé secrète en dur (ne jamais faire ça en prod)
SECRET_KEY = "super-secret-key-1234"
ADMIN_PASSWORD = "admin123"
DB_PATH = "users.db"


def get_db():
    return sqlite3.connect(DB_PATH)


# --- Auth -------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():
    """Authentification utilisateur."""
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = get_db()
    # ⚠️  SQL Injection : concaténation directe sans paramétrage
    query = "SELECT * FROM users WHERE name='" + username + "' AND password='" + password + "'"
    rows = conn.execute(query).fetchall()

    if rows:
        # ⚠️  Mot de passe affiché en clair dans les logs
        print(f"[LOGIN] User {username} logged in with password: {password}")
        return jsonify({"token": SECRET_KEY, "user": username})

    return jsonify({"error": f"User not found in {DB_PATH}"}), 401


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
    conn = get_db()
    # ⚠️  SQL Injection à nouveau
    rows = conn.execute(f"SELECT * FROM users WHERE name='{username}'").fetchall()
    if rows:
        return jsonify({"id": rows[0][0], "name": rows[0][1], "email": rows[0][2]})
    return jsonify({"error": "Not found"}), 404


# --- Fichiers ----------------------------------------------------------------

@app.route("/file", methods=["GET"])
def read_file():
    """Lit un fichier depuis le serveur."""
    filename = request.args.get("name", "")
    # ⚠️  Path traversal : pas de validation du chemin
    with open(filename, "r") as f:
        return f.read()


# --- Système -----------------------------------------------------------------

@app.route("/ping", methods=["GET"])
def ping():
    """Ping une adresse IP."""
    host = request.args.get("host", "localhost")
    # ⚠️  Command injection : input utilisateur dans un shell
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result.decode()


@app.route("/export", methods=["GET"])
def export():
    """Exporte les données en CSV."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM users").fetchall()
    output = "id,name,email,password\n"
    for r in rows:
        # ⚠️  Mots de passe exportés en clair dans le CSV
        output += f"{r[0]},{r[1]},{r[2]},{r[3]}\n"
    return output, 200, {"Content-Type": "text/csv"}


if __name__ == "__main__":
    # ⚠️  Debug mode activé en production
    app.run(debug=True, host="0.0.0.0", port=5000)
