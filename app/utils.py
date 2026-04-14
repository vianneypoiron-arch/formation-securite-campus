"""
Fonctions utilitaires.
"""

import os
import hashlib
import requests
import xml.etree.ElementTree as ET   # ⚠️  Vulnérable aux attaques XXE
import pickle                         # ⚠️  pickle est dangereux sur des données non fiables
import tempfile


# ─── Hachage ────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    # ⚠️  MD5 : algorithme cryptographiquement cassé
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


# ─── Parsing XML ────────────────────────────────────────────────────────────

def parse_user_xml(xml_string: str) -> dict:
    """Parse un profil utilisateur au format XML."""
    # ⚠️  XXE (XML External Entity) : un attaquant peut lire des fichiers du serveur
    root = ET.fromstring(xml_string)
    return {
        "name":  root.findtext("name"),
        "email": root.findtext("email"),
    }


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
