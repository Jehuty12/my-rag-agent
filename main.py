# ======================= CONFG =======================
from ollama import Client
from fastapi import FastAPI
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
from pypdf import PdfReader
from dotenv import load_dotenv

# Charge les variables d'env
load_dotenv()

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

# Crée les dossiers s'ils n'existent pas
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_PATH, exist_ok=True)

# Init ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name="my_collection")

# Init Ollama
ollama_client = Client(host=OLLAMA_HOST)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ======================= FONCTIONS =======================
def load_documents():
    with open("test_doc.txt", "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(ids=[f"doc_{i}"], documents=[chunk])

    return {"status": f"✅ {len(chunks)} chunks chargés"}

def search_documents(query: str):
    results = collection.query(query_texts=[query], n_results=3)
    return results["documents"][0] if results["documents"] else []

def generate_answer_with_context(question: str):
    # Cherche les chunks pertinents
    chunks = search_documents(question)

    # Prépare le contexte
    context = "\n".join(chunks) if chunks else "Aucun contexte trouvé"

    # Prompt avec contexte
    prompt = f"""Tu es un assistant IA utile basé sur des documents.

CONTEXTE:
{context}

QUESTION: {question}

Réponds basé sur le contexte fourni. Si la réponse ne se trouve pas dans le contexte, dis-le."""

    # Génère la réponse
    response = ollama_client.generate(
        model=OLLAMA_MODEL,
        prompt=prompt,
        stream=False
    )

    return response["response"]

def extract_text_from_file(file_path: str) -> str:
    """Extrait du texte d'un PDF ou fichier texte"""
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        # Fichier texte
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def chunk_and_store(text: str, source_name: str):
    """Découpe le texte en chunks et les stocke dans ChromaDB"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"{source_name}_{i}"],
            documents=[chunk],
            metadatas=[{"source": source_name}]
        )

    return len(chunks)

# ======================= ENDPOINTS =======================
# @app.get("/")
# def read_root():
#     return {"Hello": "hello, RAG Agent!"}
@app.get("/")
def serve_root():
    return FileResponse("static/index.html")

@app.post("/load")
def load():
    return load_documents()

@app.get("/search")
def search(q: str):
    results = search_documents(q)
    return {"query": q, "results": results}

@app.post("/ask")
def ask(question: str):
    try:
        answer = generate_answer_with_context(question)
        chunks = search_documents(question)
        return {
            "question": question,
            "answer": answer,
            "sources": chunks
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Sauvegarde le fichier
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extrait et charge le texte
        text = extract_text_from_file(file_path)
        chunks_count = chunk_and_store(text, file.filename)

        return {
            "status": f"✅ {file.filename} chargé ({chunks_count} chunks)",
            "filename": file.filename
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/documents")
def list_documents():
    """Liste tous les documents chargés"""
    try:
        # Récupère tous les documents avec leurs métadonnées
        all_data = collection.get()
        
        # Déduplique par source
        sources = {}
        for metadata, document in zip(all_data["metadatas"], all_data["documents"]):
            source = metadata.get("source", "unknown") if metadata else "unknown"
            if source not in sources:
                sources[source] = {
                    "name": source,
                    "chunks": 0,
                    "preview": document[:100] + "..."
                }
            sources[source]["chunks"] += 1
        
        return {"documents": list(sources.values())}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/documents/{doc_name}")
def delete_document(doc_name: str):
    """Supprime tous les chunks d'un document"""
    try:
        all_data = collection.get()

        ids_to_delete = []
        for metadata, id_ in zip(all_data["metadatas"], all_data["ids"]):
            source = metadata.get("source", "unknown") if metadata else "unknown"
            if source == doc_name:
                ids_to_delete.append(id_)

        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
            return {"status": f"✅ {doc_name} supprimé ({len(ids_to_delete)} chunks)"}
        else:
            return {"error": "Document non trouvé"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/config")
def get_config():
    """Retourne la configuration actuelle"""
    return {
        "ollama_host": OLLAMA_HOST,
        "ollama_model": OLLAMA_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP
    }

@app.post("/config")
def update_config(model: str = None, chunk_size: int = None, chunk_overlap: int = None):
    """Met à jour la configuration"""
    global OLLAMA_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
    
    if model:
        OLLAMA_MODEL = model
    if chunk_size:
        CHUNK_SIZE = chunk_size
    if chunk_overlap:
        CHUNK_OVERLAP = chunk_overlap
    
    return {
        "status": "✅ Configuration mise à jour",
        "config": {
            "ollama_model": OLLAMA_MODEL,
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        }
    }