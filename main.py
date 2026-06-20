from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Railway Test Success"}

@app.get("/health")
def health():
    return {"status": "ok"}