#!/bin/sh
set -e

# Controllo variabili richieste
if [ -z "$SSH_USER" ] || [ -z "$SSH_HOST" ]; then
  echo "Devi impostare SSH_USER e SSH_HOST"
  exit 1
fi

# Porta locale e remota per Kafka
LOCAL_PORT="${LOCAL_PORT:-9092}"
REMOTE_PORT="${REMOTE_PORT:-9092}"

echo "Avvio tunnel SSH: localhost:${LOCAL_PORT} -> ${SSH_HOST}:${REMOTE_PORT} (utente: ${SSH_USER})"

# Avvio tunnel in background
ssh -o StrictHostKeyChecking=accept-new \
    -o ExitOnForwardFailure=yes \
    -N \
    -L ${LOCAL_PORT}:localhost:${REMOTE_PORT} \
    -i /ssh/id_ed25519 \
    "${SSH_USER}@${SSH_HOST}" &

SSH_PID=$!
echo "Tunnel SSH PID=${SSH_PID}"

# Se il tunnel muore, vogliamo fallire
sleep 2
if ! kill -0 "$SSH_PID" 2>/dev/null; then
  echo "Il tunnel SSH non è partito correttamente"
  exit 1
fi

# Avvio il consumer
python /app/receiver.py &

APP_PID=$!

# Propaga SIGINT/SIGTERM
trap "echo 'Segnale ricevuto, chiudo...'; kill $APP_PID $SSH_PID 2>/dev/null || true; wait; exit 0" INT TERM

wait $APP_PID || true
echo "Consumer terminato, chiudo tunnel SSH..."
kill $SSH_PID 2>/dev/null || true
wait || true
echo "Bye."
