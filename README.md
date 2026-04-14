# StartupDemo — Dépôt d'atelier sécurité

> **⚠️ Dépôt intentionnellement vulnérable — usage pédagogique uniquement.**
> Ne jamais déployer ce code en production.

Petite API Flask fictive d'une startup. Elle gère des utilisateurs, une authentification et quelques endpoints utilitaires. Elle contient **volontairement de nombreuses failles de sécurité** pour l'exercice d'audit.

---

## Installation

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd demo_repo

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base
python app/database.py

# Lancer l'API
python app/main.py
```

---

## Structure

```
demo_repo/
├── app/
│   ├── main.py       # Routes Flask principales
│   ├── database.py   # Init BDD + credentials
│   ├── config.py     # Configuration (clés, secrets…)
│   └── utils.py      # Fonctions utilitaires
├── tests/
│   └── test_api.py   # Tests basiques
├── requirements.txt  # Dépendances (avec CVE !)
└── README.md
```

---

## Atelier — Consignes

### Étape 1 — Analyse statique avec Bandit

```bash
pip install bandit
bandit -r . -f json -o rapport_bandit.json
bandit -r . -ll        # affiche seulement MEDIUM et HIGH
```

**Questions :**
- Combien d'issues HIGH Bandit détecte-t-il ?
- Quels fichiers sont les plus problématiques ?
- Quels Test IDs reviennent le plus souvent ?

---

### Étape 2 — Audit des dépendances

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

**Questions :**
- Combien de CVE sont détectées ?
- Quelle dépendance a le score CVSS le plus élevé ?
- Lesquelles ont une version corrigée disponible ?

---

### Étape 3 — Correction

Choisissez **2 vulnérabilités** et proposez une correction :

1. Modifiez le code
2. Relancez Bandit — vérifiez que l'issue disparaît
3. Documentez votre correction dans un commentaire `# FIXED:`

---

## Corrigé (pour le formateur)

| Fichier | Ligne | Vulnérabilité | Sévérité Bandit | Correction |
|---|---|---|---|---|
| main.py | 32 | SQL Injection (B608) | HIGH | Utiliser des paramètres `?` |
| main.py | 38 | Password en clair dans logs (B106) | MEDIUM | Supprimer le print |
| main.py | 57 | Command injection (B602) | HIGH | subprocess sans shell=True |
| main.py | 50 | Path traversal | MEDIUM | Valider/filtrer le chemin |
| database.py | 14 | Hardcoded credentials (B105) | HIGH | Variables d'environnement |
| database.py | 24 | MD5 pour mots de passe (B303) | MEDIUM | bcrypt ou argon2 |
| utils.py | 16 | MD5 (B303) | MEDIUM | bcrypt ou argon2 |
| utils.py | 29 | XXE via ElementTree (B313) | HIGH | defusedxml |
| utils.py | 39 | Pickle non sécurisé (B301) | HIGH | json ou autre format sûr |
| utils.py | 48 | SSL verify=False (B501) | HIGH | Retirer verify=False |
| utils.py | 55 | mktemp TOCTOU (B306) | MEDIUM | tempfile.mkstemp() |
| config.py | 22 | Hardcoded secrets (B105) | HIGH | os.environ.get() |
