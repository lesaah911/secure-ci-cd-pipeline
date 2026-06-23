# Secure CI/CD Pipeline

Pipeline CI/CD avec scans de sécurité automatisés — Jenkins + Docker + Gitleaks + Trivy + Semgrep.

## Objectif

Mettre en place un pipeline d'intégration continue qui **détecte et bloque automatiquement** les vulnérabilités à chaque push de code, avant tout déploiement. Chaque étape de sécurité est bloquante : si une faille critique est détectée, le pipeline s'arrête.

## Architecture

```
GitHub push
    │
    ▼
Jenkins Pipeline
    │
    ├── Scan secrets (Gitleaks)
    │       └── Détecte les secrets/tokens oubliés dans le code
    │
    ├── Build (Docker)
    │       └── Construction de l'image de l'application
    │
    ├── Scan image (Trivy)
    │       └── Détecte les CVE dans l'image et les dépendances
    │       └── Bloque sur CRITICAL / HIGH
    │
    └── Scan code (Semgrep)
            └── Analyse statique du code source (SAST)
            └── Détecte injections, mauvaises pratiques Flask, etc.
```

## Stack technique

| Composant | Rôle |
|-----------|------|
| Jenkins (conteneur) | Orchestration du pipeline |
| Docker | Build et déploiement de l'application |
| Gitleaks | Scan de secrets dans le code source |
| Trivy | Scan de vulnérabilités (CVE) sur l'image Docker |
| Semgrep | Analyse statique du code (SAST) |
| GitHub | Hébergement du code, déclenchement du pipeline |

## Résultats — ce que le pipeline a détecté et corrigé

### Cycle 1 : Vulnérabilités dans l'image Docker

Trivy a détecté **2 CRITIQUE + 9 ÉLEVÉE** sur l'image de base `python:3.12-slim` (Perl, ncurses, SQLite embarqués inutilement).

**Correction** : passage à `python:3.12-alpine` (image minimaliste sans paquets superflus).

**Résultat** : 0 CVE CRITICAL/HIGH détectée.

### Cycle 2 : Failles dans le code source

Semgrep a détecté **2 failles** dans `app.py` :

- **Injection de commande** — données utilisateur injectées directement dans `os.popen()`, permettant une exécution de commande arbitraire
- **Exposition réseau** — serveur Flask exposé sur `0.0.0.0` (toutes les interfaces)

**Build #10 — failles détectées :**

![Pipeline build #10](docs/1.png)

![Semgrep findings build #10](docs/2.png)

**Correction** :
- `os.popen(f"ping -c 1 {host}")` remplacé par `subprocess.run(["ping", "-c", "1", host], ...)` — plus d'injection possible, chaque argument est isolé
- `host="0.0.0.0"` remplacé par `host="127.0.0.1"` — écoute locale uniquement

**Build #11 — pipeline vert après correction :**

![Pipeline build #11](docs/3.png)

![Semgrep 0 résultat build #11](docs/4.png)

## Structure du repo

```
.
├── app.py                  # Application Flask (cible du pipeline)
├── requirements.txt        # Dépendances Python
├── Dockerfile              # Image de l'application (python:3.12-alpine)
├── Jenkinsfile             # Définition du pipeline CI/CD
└── docs/                   # Captures des résultats de scan
```

## Lancer le projet en local

### Prérequis
- Docker Desktop
- Git

### Démarrer Jenkins

```bash
# Cloner le repo
git clone https://github.com/lesaah911/secure-ci-cd-pipeline.git
cd secure-ci-cd-pipeline

# Démarrer Jenkins
docker compose up -d

# Récupérer le mot de passe initial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Accéder à Jenkins sur `http://localhost:8080`, configurer le job en pointant sur ce repo (branch : `main`, script : `Jenkinsfile`).

### Builder l'application seule

```bash
docker build -t secure-app .
docker run -d -p 5000:5000 secure-app
curl http://localhost:5000
```

## Points clés DevSecOps

- **Shift-left** : les scans de sécurité s'exécutent avant le déploiement, pas après
- **Gate bloquant** : Trivy avec `--exit-code 1` stoppe le pipeline sur CRITICAL/HIGH
- **Image minimaliste** : Alpine réduit la surface d'attaque par rapport à Debian slim
- **SAST intégré** : Semgrep analyse le code à chaque commit, pas ponctuellement
- **Infrastructure as Code** : Jenkins lui-même est conteneurisé et reproductible

## Auteur

Émeric Saah — Mastère Cybersécurité IPSSI Paris (2025-2027)
