from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "IHMP Backend is running on FastAPI 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
