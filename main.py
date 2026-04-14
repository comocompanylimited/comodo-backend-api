import os
from fastapi import FastAPI

app = FastAPI(title="Comodo Master Backend")

port = int(os.environ.get("PORT", 8000))


@app.get("/")
def read_root():
    return {"message": "Comodo Master Backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
