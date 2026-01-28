#!/bin/sh

set -eu

# =========================
# FESTE GIT-KONFIGURATION
# =========================
GIT_NAME="Tjark Brendel"
GIT_EMAIL="mail@tjark-brendel.de"

echo "==> Prüfe Git"
git --version
echo ""

echo "==> Setze Git-Konfiguration"
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

git config --global init.defaultBranch main
git config --global core.editor nano
git config --global color.ui auto

echo "==> Git-Konfiguration:"
git config --global --list
echo ""

# =========================
# PAKETE INSTALLIEREN
# =========================
echo "==> Aktualisiere Paketliste"
apk update

echo "==> Installiere python3"
apk add --no-cache python3

echo "==> Installiere nano"
apk add --no-cache nano

# =========================
# CHECKS
# =========================
echo ""
echo "==> Checks"
python3 --version
nano --version | head -n 1
git --version

echo ""
echo "==> SYSTEM BEREIT"
echo "Du kannst jetzt:"
echo "  - Python-Skripte ausführen (python3 script.py)"
echo "  - Dateien mit nano bearbeiten"
echo "  - Git normal nutzen (add / commit / push)"
