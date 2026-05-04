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

# init chromadb (stockage local)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="my_collection")

ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama_client = Client(host=ollama_host)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ======================= FONCTIONS =======================
def load_documents():
    with open("test_doc.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
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
        model="mistral",
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
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
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
        file_path = f"uploads/{file.filename}"
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