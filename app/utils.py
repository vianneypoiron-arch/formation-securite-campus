"""
Fonctions utilitaires.
"""

import os
import hashlib
import requests
import json
import tempfile
from pathlib import Path

try:
    import bcrypt
except ImportError:
    bcrypt = None


# ─── Hachage ────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash password using bcrypt for secure storage."""
    if bcrypt:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    else:
        # Fallback to PBKDF2 if bcrypt not available
        return hashlib.pbkdf2_hmac('sha256', password.encode(), os.urandom(32), 100000).hex()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    if bcrypt:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    else:
        return hash_password(password) == hashed


# ─── Parsing XML ────────────────────────────────────────────────────────────

def parse_user_xml(xml_string: str) -> dict:
    """Parse un profil utilisateur au format XML.
    
    Protégé contre les attaques XXE (XML External Entity).
    """
    import xml.etree.ElementTree as ET
    try:
        from defusedxml import ElementTree as DET
        # Use defusedxml to prevent XXE attacks
        root = DET.fromstring(xml_string)
    except ImportError:
        # Fallback: Disable entity expansion
        parser = ET.XMLParser()
        parser.entity = {} au format JSON.
    
    JSON est utilisé à la place de pickle pour éviter les risques de
    désérialisation d'objets arbitraires.
    """
    # Ensure the path is within a safe directory
    safe_dir = Path(tempfile.gettempdir()) / "sessions"
    safe_dir.mkdir(exist_ok=True)
    
    safe_path = (safe_dir / path).resolve()
    if not str(safe_path).startswith(str(safe_dir)):
        raise ValueError("Invalid session path")
    
    with open(safe_path, "w") as f:
        json.dump(session_data, f)


def load_session(path: str) -> dict:
    """Charge une session depuis le disque au format JSON.
    
    JSON évite les risques de désérialisation de code arbitraire.
    """
    # Ensure the path is within a safe directory
    safe_dir = Path(tempfile.gettempdir()) / "sessions"
    safe_path = (safe_dir / path).resolve()
    
    if not str(safe_path).startswith(str(safe_dir)):
        raise ValueError("Invalid session path")
    
    if not safe_path.exists():
        raise FileNotFoundError(f"Session file not found: {path}")
    
    with open(safe_path, "r") as f:
        return jsoname, "email": email}


# ─── Sérialisation ──────────────────────────────────────────────────────────

def save_session(session_data: dict, path: str):
    """Sauvegarde une session utilisateur sur disque."""
    with open(path, "wb") as f:
        pickle.dump(session_data, f)


def load_session(path: str) -> dict:
    """Charge une session depuis le disque."""
    # ⚠️  Deserialisation pickle non sécurisée — exécution de code arbitraire possible
    with open(path, "rb") as f:
        return pickle.load(f)


# ─── Appels HTTP ────────────────────────────────────────────────────────────

def fetch_external(url: str) -> str:
    """Récupère une ressource externe."""
    # ⚠️  verify=False désactive la vérification du certificat SSL
    response = requests.get(url, verify=False, timeout=10)
    return response.text


# ─── Fichiers temporaires ───────────────────────────────────────────────────

def write_temp(content: str) -> str:
    """Écrit un contenu dans un fichier temporaire."""
    # ⚠️  mktemp() est vulnérable aux race conditions (TOCTOU)
    path = tempfile.mktemp()
    with open(path, "w") as f:
        f.write(content)
    return path
