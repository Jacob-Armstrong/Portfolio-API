from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine

def create_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="Welcome to my portfolio!"
)

@app.get("/")
async def root():
    return {
        "Introduction": "Welcome to my Portfolio! This is an interactive API to get more information about me, or leave a message saying you visted!",
        "Created by": "Jacob Armstrong",
        "Using": "FastAPI, Pydantic, SQLModel and PostgreSQL",
        "Documentation": ""
    }

if __name__ == "__main__":
    create_db()