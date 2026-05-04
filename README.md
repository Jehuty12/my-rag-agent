# 🤖 RAG Agent — Assistant IA avec contexte

Un assistant IA local qui ingère des documents et répond avec du contexte. Déployé en API FastAPI, utilisant ChromaDB pour le stockage vectoriel et Ollama pour le LLM local.

## 📊 Stack

- **FastAPI** — API web moderne et rapide
- **ChromaDB** — Base de données vectorielles (stockage local)
- **Ollama** — LLM local gratuit (Llama 2, Mistral, etc.)
- **Langchain** — Orchestration du RAG
- **Docker** — Déploiement en conteneur

## 🚀 Étapes complétées

### ✅ Étape 1 : Setup + Première API
- Création de l'environnement Python
- Installation de FastAPI et Uvicorn
- Route GET simple `/` qui retourne "Hello, RAG Agent!"
- Route GET `/ask` pour poser des questions (placeholder)

### ✅ Étape 2 : Charger des documents dans ChromaDB
- Installation de ChromaDB et Langchain
- Découpe du texte en chunks (100 caractères, overlap 20)
- Chargement automatique des embeddings
- Route POST `/load` pour charger les documents
- Route GET `/search?q=...` pour chercher les chunks pertinents

**Résultat :** Les 5 chunks du document test sont chargés et recherchables par similarité sémantique.

### ✅ Étape 3 : Connecter Ollama — RAG complet
- Installation de Docker et lancement du conteneur Ollama
- Téléchargement du modèle Mistral (~5 GB)
- Intégration avec FastAPI via la client Ollama Python
- Route POST `/ask?question=...` qui :
  1. Cherche les chunks pertinents dans ChromaDB
  2. Envoie les chunks + la question à Ollama
  3. Retourne la réponse générée avec contexte + sources

**Résultat :** RAG fonctionnel ! 
```json
{
  "question": "Qu'est-ce que Python",
  "answer": "Python est un langage de programmation créé en 1991 qui est très populaire pour la data science et l'IA.",
  "sources": ["Python est très populaire...", "Python est un langage..."]
}
```

### ✅ Étape 4 : Finitions et déploiement
- Créé `requirements.txt` avec toutes les dépendances
- Nettoyé et structuré le code `main.py` avec commentaires
- Créé `Dockerfile` pour déployer l'app dans un conteneur
- Créé `docker-compose.yml` pour orchestrer Ollama + FastAPI
- ✅ Testé en Docker — tout fonctionne !

**Déploiement facile :**
```bash
docker-compose up
```

L'API est accessible sur `http://localhost:8000`

---

## 🎯 Projet complété et fonctionnel en production ! 🚀

**Stack en production :**
- **Ollama + Mistral** (LLM local, gratuit, 7B paramètres)
- **ChromaDB** (stockage vectoriel avec embeddings automatiques)
- **FastAPI** (API web moderne et rapide)
- **Docker + Docker Compose** (déploiement one-click)

**Endpoints pleinement testés :**
- `POST /load` — Charger et ingérer des documents
- `GET /search?q=...` — Rechercher dans ChromaDB (similarité sémantique)
- `POST /ask?question=...` — **RAG complet** (recherche + génération intelligente)

### 📝 Exemple de résultat :
```json
{
  "question": "Dis-moi ce que tu sais sur ChromaDB",
  "answer": "ChromaDB est une base de vecteurs simple, locale et gratuite...",
  "sources": [
    "ChromaDB est une base vecteurs facile, locale et gratuite.",
    "FastAPI est un framework web moderne et très performant.",
    "Python est très populaire pour la data science et l'IA."
  ]
}
```

## 📊 Points forts du projet

✅ **Zéro coût** — Tout gratuit (Ollama, ChromaDB, FastAPI, Docker)  
✅ **Production-ready** — Déploiement en un seul `docker-compose up`  
✅ **RAG complet** — Génération avec contexte (pas juste de la recherche)  
✅ **Scalable** — Facile d'ajouter plus de documents, changer le modèle, etc.  
✅ **Local** — Aucune API externe, données privées  

## 🎓 Ce que tu as appris

- FastAPI et création d'API web en Python
- Embeddings et recherche sémantique (ChromaDB)
- Orchestration de conteneurs (Docker + Docker Compose)
- RAG (Retrieval-Augmented Generation) — la base de la plupart des assistants IA modernes
- Intégration avec LLM locaux (Ollama)

## 🛠️ Setup local

### Prérequis
- Python 3.11+
- pip

### Installation
```bash
# Cloner le repo
cd my-rag-agent

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install fastapi uvicorn chromadb langchain-text-splitters pypdf
```

### Lancer le serveur
```bash
uvicorn main:app --reload
```

L'API est accessible sur `http://127.0.0.1:8000`

### Endpoints actuels

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Test de l'API |
| POST | `/load` | Charger les documents dans ChromaDB |
| GET | `/search?q=...` | Chercher des chunks pertinents |

## 📁 Structure du projet

```
my-rag-agent/
├── main.py              # Code principal FastAPI
├── test_doc.txt         # Document de test
├── chroma_data/         # Stockage ChromaDB (auto-généré)
├── venv/                # Environnement Python
├── README.md            # Ce fichier
└── requirements.txt     # (À faire) Liste des dépendances
```

## 🧠 Comment ça marche

1. **Chargement** : Les documents sont découpés en chunks et les embeddings sont calculés automatiquement par ChromaDB
2. **Recherche** : ChromaDB trouve les chunks les plus proches sémantiquement de la question
3. **Génération** : (Étape 3) Les chunks + la question sont envoyés à Ollama pour générer une réponse avec contexte

---

# 🎬 PHASE 2 — L'app réelle (utilisable par n'importe qui)

## 🚀 Améliorations en cours

### ✅ Étape 5 : Front web simple (HTML/CSS/JS)
- Interface web pour poser des questions sans curl
- Upload de documents via drag-and-drop
- Affichage des réponses + sources en temps réel

### ✅ Étape 6 : Support des PDFs réels
- Charger des PDFs, TXT, sans limite
- Extraction automatique du contenu
- Feedback visuel des fichiers sélectionnés
- Preview avant chargement

### ⏳ Étape 7 : Multi-documents
- Lister les documents chargés
- Supprimer/recharger des documents
- Afficher la source de chaque réponse

### ⏳ Étape 8 : Optimisations
- Meilleur prompt pour réponses courtes & précises
- Chunks ajustables (taille/overlap)
- Possibilité de changer le modèle Ollama (Mistral → Llama 2, etc.)

### ⏳ Phase 3 : Deploy en cloud (optionnel)
- Mettre en ligne sur Railway, Render, etc.
