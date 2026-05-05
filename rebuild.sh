#!/bin/bash

echo ""
echo "========================================"
echo "  🔄 RAG Agent - Full Rebuild"
echo "========================================"
echo ""

docker-compose down
docker-compose build --no-cache
docker-compose up

echo ""
echo "✅ Rebuild complet terminé!"
echo ""
