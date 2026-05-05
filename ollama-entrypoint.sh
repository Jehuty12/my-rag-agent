#!/bin/bash
set -e

echo "🚀 Démarrage d'Ollama..."
ollama serve &
OLLAMA_PID=$!

echo "⏳ Attente du démarrage d'Ollama..."
sleep 3

# Attends que le serveur soit prêt
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama est prêt!"
    break
  fi
  echo "⏳ Tentative $i/30..."
  sleep 2
done

echo "📥 Téléchargement du modèle mistral..."
ollama pull mistral

echo "✅ Modèle mistral téléchargé!"
echo ""
echo "🤖 RAG Agent est maintenant prêt!"
echo "Ouvre http://localhost:8000"
echo ""

# Garde Ollama au foreground
wait $OLLAMA_PID
