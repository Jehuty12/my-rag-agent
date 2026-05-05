# 🤖 RAG Agent — Assistant IA Local avec Contexte

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un **assistant IA local et privé** qui ingère vos documents (PDF, TXT) et répond avec contexte. Zéro API externe, zéro coût, 100% local.

## ✨ Caractéristiques

- ✅ **RAG complet** — Retrieval-Augmented Generation pour réponses contextualisées
- ✅ **Modèles locaux** — Ollama + Mistral/Llama 2 (gratuit, offline)
- ✅ **Multi-documents** — Gérer plusieurs PDFs/fichiers simultanément
- ✅ **Configuration dynamique** — Ajuster chunks, modèle, prompts en temps réel
- ✅ **Interface web** — UI moderne et intuitive (drag-drop, aperçu temps réel)
- ✅ **Docker ready** — Deploy en 1 commande
- ✅ **Zéro coût** — Tout gratuit et open-source

## 🚀 Quick Start

### Prérequis
- Docker & Docker Compose
- ~6 GB d'espace disque (pour Mistral)

### Installation & lancement

```bash
# 1. Clone le repo
git clone https://github.com/yourusername/rag-agent.git
cd rag-agent

# 2. Copie la configuration
cp .env.sample .env

# 3. Lance avec un click (Windows) ou avec bash
rebuild.bat          # Windows
# ou
bash rebuild.sh      # Mac/Linux

# 4. Ouvre le navigateur
http://localhost:8000
```

**C'est tout !** L'app démarre en ~2-3 minutes la première fois (télécharge Mistral).

## 📖 Utilisation

### Interface Web
1. **Charger des documents** — Drag-drop des PDFs ou TXT
2. **Poser une question** — L'IA cherche dans vos docs et répond
3. **Configurer** — Ajuster modèle, chunk size, overlap
4. **Gérer** — Voir tous les docs, supprimer ceux dont tu as plus besoin

### API REST

```bash
# Charger des documents
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload

# Poser une question
curl -X POST "http://localhost:8000/ask?question=Qu'est-ce%20que%20Python?"

# Lister les documents
curl http://localhost:8000/documents

# Obtenir la config
curl http://localhost:8000/config

# Modifier la config
curl -X POST "http://localhost:8000/config?model=llama2&chunk_size=600"
```

## 🎛️ Comprendre la Configuration

### 📚 **Modèle Ollama**
Le "cerveau" qui répond aux questions.

- **mistral** (défaut) — Rapide, bon compromis, 7B paramètres
- **llama2** — Plus puissant mais plus lent, meilleure compréhension

```bash
# Changer le modèle via l'interface web ou API
curl -X POST "http://localhost:8000/config?model=llama2"
```

### 🔪 **Chunk Size (Taille des morceaux)**
Comme découper un livre en pages — détermine la "mémoire" du RAG.

| Taille | Effet | Recommandé |
|--------|-------|-----------|
| 100-200 | Contexte faible, fragmenté | ❌ |
| **400-800** | **Équilibre parfait** | **✅** |
| 2000+ | Bruit, l'IA se perd | ❌ |

### 🔗 **Chunk Overlap (Chevauchement)**
Débordement entre chunks pour garder le contexte à la jonction.

**Recommandé:** 10-20% de chunk_size (ex: 50-100 pour 500)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│            Web UI (HTML/CSS/JS)                 │
│         http://localhost:8000                   │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│          FastAPI Server (Python)                │
│  - Upload & Parsing (PDF, TXT)                  │
│  - Document Management                          │
│  - RAG Pipeline Orchestration                   │
└────────────┬──────────────────┬────────────────┘
             │                  │
    ┌────────▼──────┐    ┌──────▼────────┐
    │  ChromaDB     │    │  Ollama       │
    │  (Vecteurs)   │    │  (LLM Local)  │
    │  Embeddings   │    │  Mistral/Llama│
    └───────────────┘    └───────────────┘
```

## 📋 Structure du Projet

```
rag-agent/
├── main.py                  # API FastAPI + logique RAG
├── static/
│   └── index.html          # Interface web
├── Dockerfile              # Image Docker
├── docker-compose.yml      # Orchestration
├── requirements.txt        # Dépendances Python
├── .env.sample             # Config exemple
├── .gitignore              # Fichiers ignorés
├── rebuild.bat/.sh         # Script de rebuild
└── README.md               # Ce fichier
```

## 🛠️ Installation Manuelle (sans Docker)

Si tu préfères sans Docker :

```bash
# 1. Python 3.11+
python --version

# 2. Installe les dépendances
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Ollama local
# Télécharge depuis https://ollama.ai
ollama pull mistral

# 4. Lance le serveur
uvicorn main:app --reload

# 5. Ouvre http://localhost:8000
```

## 📝 Convention des Commits

Ce projet utilise **Conventional Commits** pour une meilleure traçabilité.

### Format
```
<type>(<scope>): <description>
```

### Types
- `feat` — Nouvelle fonctionnalité
- `fix` — Bug fix
- `docs` — Documentation
- `refactor` — Refactorisation
- `perf` — Performance
- `test` — Tests
- `chore` — Dépendances, build

### Exemples
```
feat(config): add dynamic chunk size adjustment
fix(documents): handle None metadata in deletion
docs(readme): add architecture diagram
```

## 🚢 Déploiement

### Docker (local)
```bash
docker-compose up
```

### Kubernetes (cloud)
Un fichier Helm chart est en préparation pour déployer sur Kubernetes.

```bash
# À venir
helm install rag-agent ./helm
```

### Railway / Render (cloud)
1. Push ce repo sur GitHub
2. Connecte Railway/Render à ton repo
3. Configure les variables d'env
4. Deploy (auto)

## 🔐 Variables d'Environnement

Voir `.env.sample` pour les options complètes :

```env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=mistral
CHUNK_SIZE=500
CHUNK_OVERLAP=50
UPLOAD_DIR=uploads
CHROMA_DB_PATH=chroma_db
```

## 📊 Performance

| Opération | Temps (Mistral) | Notes |
|-----------|-----------------|-------|
| Upload PDF (1 MB) | ~500ms | Extraction + parsing |
| Indexation (100 chunks) | ~1s | Calcul embeddings |
| Recherche (3 chunks) | ~50ms | Query ChromaDB |
| Génération réponse | ~3-5s | Dépend de la longueur |

**Total:** ~4-6s de la question à la réponse

## 🤝 Contribution

Les PRs sont les bienvenues ! Pour des changements majeurs :

1. Fork le repo
2. Crée une branche (`git checkout -b feat/amazing-feature`)
3. Commit avec Conventional Commits
4. Push et crée une PR

## 📜 License

MIT License — Voir [LICENSE](LICENSE) pour les détails.

## 🙋 Support

- 📖 [Documentation](README.md)
- 🐛 [Issues](https://github.com/yourusername/rag-agent/issues)
- 💬 Discussions bienvenues

## 🎓 Apprentissage

Ce projet est parfait pour apprendre :
- **RAG** — Comment combiner recherche + génération IA
- **FastAPI** — Framework web moderne Python
- **Docker** — Containerization & orchestration
- **Vector DBs** — ChromaDB & embeddings
- **LLMs** — Utiliser des modèles locaux

## 📚 Ressources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Ollama](https://ollama.ai/)
- [ChromaDB](https://www.trychroma.com/)

---

⭐ Si tu aimes ce projet, n'hésite pas à laisser une star !
