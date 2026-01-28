#!/bin/sh
set -eu

OPENAI_API_KEY="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"


###############################################################################
# askgpt.sh - CLI-Klausurassistent (Alpine / BusyBox sh)
# Dependencies: curl, jq
###############################################################################

# Modell (kannst du per ENV überschreiben: MODEL=... ./askgpt.sh)
MODEL="${MODEL:-gpt-5.2-2025-12-11}"

# Wo Verlauf gespeichert wird
HIST_FILE="${HIST_FILE:-$HOME/.askgpt_history.json}"
MAX_TURNS="${MAX_TURNS:-10}"   # wie viele (user+assistant)-Paare im Kontext bleiben

# Default-Modus
MODE="${MODE:-normal}"

# Globaler "Klausurassistent"-Systemprompt (Basis)
BASE_SYSTEM_PROMPT='Du bist ein Klausurassistent für IT-Administration (TH Wildau). Antworte prüfungsorientiert, konkret und kompakt:
- Erst: direkte Antwort/Lösung (1–3 Zeilen).
- Dann: minimal Begründung/Definition (max. 5 Zeilen).
- Dann: falls passend: Befehle/Kommandos als Copy-Paste-Block.
- Keine langen Romane, keine unnötige Theorie. Wenn etwas unklar ist, stelle max. 1 kurze Rückfrage, ansonsten triff die wahrscheinlichste Annahme und markiere sie als Annahme.'

# Mode-spezifische Zusätze
MODE_NORMAL='Fokus: Allgemein Klausurhilfe, kompakte Antworten, Schritt-für-Schritt nur wenn nötig.'
MODE_PYTHON='Fokus: Python-Klausurhilfe. Erkläre Code Schritt für Schritt. Gib kurze, abschreibbare Snippets. Nutze einfache Begriffe. Wenn mehrere Lösungen möglich: nenne die klausurtauglichste.'
MODE_CISCO='Fokus: Cisco IOS/Packet Tracer. Gib Kommandos in richtiger Reihenfolge inkl. prompt-Kontext (enable/conf t/interface). Nutze typische Klausur-Defaults (z.B. shutdown/no shutdown, ip address, vlan, trunk, access, show-Befehle).'
MODE_LINUX='Fokus: Linux-Admin. Gib konkrete Shell-Befehle, Pfade, Logs, typische Troubleshooting-Reihenfolge. Prefer BusyBox/Alpine-kompatible Befehle.'

###############################################################################
# Safety / Setup
###############################################################################
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "Fehler: OPENAI_API_KEY ist nicht gesetzt."
  echo "Setze ihn z.B. mit: export OPENAI_API_KEY='...'"
  exit 1
fi

# History initialisieren, falls nicht vorhanden
if [ ! -f "$HIST_FILE" ]; then
  printf '[]\n' > "$HIST_FILE"
fi

# Mode-Text wählen
mode_prompt() {
  case "$MODE" in
    normal) echo "$MODE_NORMAL" ;;
    python) echo "$MODE_PYTHON" ;;
    cisco)  echo "$MODE_CISCO" ;;
    linux)  echo "$MODE_LINUX" ;;
    *)      echo "$MODE_NORMAL" ;;
  esac
}

print_help() {
  cat <<EOF
Befehle:
  /help                 Hilfe anzeigen
  /exit                 Beenden (alternativ: Ctrl+C)
  /reset                Verlauf löschen
  /mode normal|python|cisco|linux   Modus umschalten
  /where                Zeigt Speicherort der History
  /show                 Zeigt die letzten Turns (kurz)

Tipps:
  - MODEL überschreiben: MODEL=gpt-5.2-2025-12-11 ./askgpt.sh
  - Verlauf-Datei: HIST_FILE=... ./askgpt.sh
  - Kontextlänge: MAX_TURNS=10 ./askgpt.sh
EOF
}

# Kürzt History auf die letzten MAX_TURNS Paare (= 2*MAX_TURNS Nachrichten)
trim_history() {
  # Keep last 2*MAX_TURNS messages
  tmp="$(mktemp)"
  jq --argjson n "$((MAX_TURNS*2))" '
    if length > $n then .[-$n:] else . end
  ' "$HIST_FILE" > "$tmp" && mv "$tmp" "$HIST_FILE"
}

append_history() {
  role="$1"
  content="$2"
  tmp="$(mktemp)"
  jq --arg role "$role" --arg content "$content" '
    . + [{"role": $role, "content": $content}]
  ' "$HIST_FILE" > "$tmp" && mv "$tmp" "$HIST_FILE"
  trim_history
}

# Extrahiert Text aus Responses API robust
extract_answer() {
  jq -r '
    (.output_text // empty)
    // ([.output[]?
          | select(.type=="message")
          | .content[]?
          | select(.type=="output_text")
          | .text] | join("\n"))
  '
}

###############################################################################
# UI
###############################################################################
echo "Klausurassistent gestartet.  (/help | /exit | Ctrl+C)"
echo "Model: $MODEL"
echo "Mode : $MODE"
echo "History: $HIST_FILE"
echo ""

###############################################################################
# Main loop
###############################################################################
while true; do
  printf "Du> "
  IFS= read -r USER_INPUT || exit 0

  # Kommandos
  case "$USER_INPUT" in
    "/exit") exit 0 ;;
    "/help") print_help; echo ""; continue ;;
    "/reset")
      printf '[]\n' > "$HIST_FILE"
      echo "History gelöscht."
      echo ""
      continue
      ;;
    "/where")
      echo "$HIST_FILE"
      echo ""
      continue
      ;;
    "/show")
      # Kurzansicht letzte Einträge
      jq -r '.[-12:][] | "\(.role): \(.content|gsub("\n";" ")|.[0:120])"' "$HIST_FILE" 2>/dev/null || true
      echo ""
      continue
      ;;
    "/mode "*)
      NEW_MODE="$(echo "$USER_INPUT" | awk '{print $2}')"
      case "$NEW_MODE" in
        normal|python|cisco|linux)
          MODE="$NEW_MODE"
          echo "Mode gesetzt: $MODE"
          echo ""
          ;;
        *)
          echo "Unbekannter Mode: $NEW_MODE (erlaubt: normal|python|cisco|linux)"
          echo ""
          ;;
      esac
      continue
      ;;
    "")
      continue
      ;;
  esac

  # User input in history
  append_history "user" "$USER_INPUT"

  # Systemprompt (Basis + Modus)
  SYS="$BASE_SYSTEM_PROMPT

Aktueller Modus: $MODE
Mode-Regeln: $(mode_prompt)

Wenn die Frage nach Cisco/Python/Linux klingt, gib trotzdem klausurtaugliche Standardantworten und Kommandos/Beispiele."

  # Baue input: system + gesamte History (mit Rollen user/assistant)
  INPUT_JSON="$(jq -n \
    --arg model "$MODEL" \
    --arg sys "$SYS" \
    --slurpfile hist "$HIST_FILE" \
    '{
      model: $model,
      input: (
        [ {role:"system", content:$sys} ]
        + ($hist[0] // [])
      )
    }'
  )"

  RESP="$(
    curl -sS https://api.openai.com/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d "$INPUT_JSON"
  )"

  # Fehlerbehandlung
  if echo "$RESP" | jq -e '.error != null' >/dev/null 2>&1; then
    echo "Ich> API-Fehler:"
    echo "$RESP" | jq -r '.error.message // .error' 2>/dev/null || echo "$RESP"
    echo ""
    continue
  fi

  ANSWER="$(echo "$RESP" | extract_answer)"

  if [ -z "$ANSWER" ]; then
    echo "Ich> (keine Antwort extrahiert – Debug JSON folgt)"
    echo "$RESP" | jq .
    echo ""
    continue
  fi

  echo "Ich> $ANSWER"
  echo ""

  # Assistant reply in history
  append_history "assistant" "$ANSWER"
done
