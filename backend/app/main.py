from fastapi import FastAPI

app = FastAPI(title="BBDS", version="3.0")

@app.get("/")
def home():
    return {"name": "BBDS", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
