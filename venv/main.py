from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "hello, RAG Agent!"}

@app.get("/ask")
def ask(question:str):
    return {"question": question,"answer":"Je répond plus tard... "}