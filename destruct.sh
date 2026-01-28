#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ASK="$SCRIPT_DIR/askgpt.sh"
SELF="$SCRIPT_DIR/selfdestruct.sh"
HIST="${HIST_FILE:-$HOME/.askgpt_history.json}"

echo "Self-Destruct (sicher)"
echo "Lösche:"
echo "  - $ASK"
echo "  - $HIST (falls vorhanden)"
echo "  - $SELF"
echo ""
printf "Wirklich ausführen? Tippe GENAU: DELETE\n> "
IFS= read -r CONFIRM
[ "$CONFIRM" = "DELETE" ] || { echo "Abgebrochen."; exit 1; }

# Spuren entfernen
rm -f -- "$HIST"
rm -f -- "$ASK"

# Selbst löschen: in Subshell, damit rm nach Exit greifen kann
( rm -f -- "$SELF" ) >/dev/null 2>&1 || true

echo "Fertig. (Script/History entfernt)"
