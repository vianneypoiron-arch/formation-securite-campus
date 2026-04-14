"""
Configuration de l'application.
"""

# ──────────────────────────────────────────────
# Paramètres généraux
# ──────────────────────────────────────────────
APP_NAME = "StartupDemo"
VERSION = "0.3.1"
ENV = "production"

# ──────────────────────────────────────────────
# Base de données
# ──────────────────────────────────────────────
DATABASE_URL = "sqlite:///users.db"

# ──────────────────────────────────────────────
# Sécurité
# ──────────────────────────────────────────────
# ⚠️  SECRET_KEY faible et en dur
SECRET_KEY = "dev-secret-key"
JWT_EXPIRY = 99999999          # ⚠️  Token qui n'expire jamais (en secondes)
SESSION_COOKIE_SECURE = False  # ⚠️  Cookie non sécurisé (HTTPS désactivé)
CORS_ORIGINS = "*"             # ⚠️  CORS ouvert à tout le monde

# ──────────────────────────────────────────────
# Services externes
# ──────────────────────────────────────────────
# ⚠️  Credentials en dur (auraient dû être dans des variables d'environnement)
STRIPE_SECRET   = "sk_live_4xT8mZqL9bWcYnR2vKpJ3hDe"
SENDGRID_KEY    = "SG.xYz123AbcDef456GhiJkl.mNoPqRsTuVwXyZ"
OPENAI_API_KEY  = "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"
SENTRY_DSN      = "https://abc123@sentry.io/456789"

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
# ⚠️  Niveau DEBUG activé en production → expose les données sensibles dans les logs
LOG_LEVEL = "DEBUG"
LOG_FILE  = "/tmp/app.log"
