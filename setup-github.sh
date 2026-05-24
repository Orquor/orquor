#!/bin/bash
# setup-github.sh — Configurar GitHub Organization y subir repo
# Ejecutar DESPUES de crear cuenta personal en github.com

set -e

GITHUB_USER="orquor-freddy"
GITHUB_ORG="orquor"
PROJECT_DIR="/mnt/c/Users/frefe/OneDrive/Desktop/START UP/orquor"

echo "=== GitHub Setup ORQUOR ==="

# 1. Crear organization (requiere token)
echo "Necesitas crear un Personal Access Token en:"
echo "  https://github.com/settings/tokens"
echo "  Permisos: repo, admin:org"
echo ""
read -p "Pega tu token de GitHub: " TOKEN

# 2. Crear organization
curl -s -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/user/orgs \
     -d "{\"login\":\"$GITHUB_ORG\",\"billing_email\":\"freddy@orquor.com\"}" \
     | python3 -m json.tool

# 3. Crear repo
curl -s -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/orgs/$GITHUB_ORG/repos \
     -d "{\"name\":\"orquor\",\"description\":\"Multi-agent orchestration platform for regulated LATAM sectors\",\"private\":false}" \
     | python3 -m json.tool

# 4. Push
cd "$PROJECT_DIR"
git remote add origin "https://github.com/$GITHUB_ORG/orquor.git" 2>/dev/null || git remote set-url origin "https://github.com/$GITHUB_ORG/orquor.git"
git add .
git commit -m "Initial commit: ORQUOR empire foundation
- 10 carpetas, ~90 archivos
- ACTO whitepaper + PDF
- HERMES 6 sub-agents + 13 verifiers
- Content calendar 90 days
- Legal templates + Hostinger migration runbook" 2>/dev/null || echo "No changes to commit"
git branch -M main
git push -u origin main

echo "=== DONE: https://github.com/$GITHUB_ORG/orquor ==="
