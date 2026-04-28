from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AgriGPT is running successfully 🚀"}

@app.get("/test")
def test():
    return {"status": "working"}
