from fastapi import FastAPI
from .database import Base, engine

from .routers import profile, skills, education, experience

def create_db():
    Base.metadata.create_all(engine)

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="Welcome to my portfolio!"
)

# Include routers
app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(education.router)
app.include_router(experience.router)

@app.get("/")
async def root():
    return {
        "Introduction": "Welcome to my Portfolio! This is an interactive API to get more information about me, or leave a message saying you visted!",
        "Created by": "Jacob Armstrong",
        "Using": "FastAPI, Pydantic, SQLAlchemy and PostgreSQL",
        "Documentation": ""
    }

if __name__ == "__main__":
    create_db()