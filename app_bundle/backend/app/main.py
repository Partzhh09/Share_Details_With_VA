from fastapi import FastAPI
from app.api.ipo import router as ipo_router

app = FastAPI(title="IPO Predict with VA")
app.include_router(ipo_router, prefix="/ipo")

@app.get("/")
def root():
    return {"status": "Backend is running"}

# python -m uvicorn app.main:app --reload