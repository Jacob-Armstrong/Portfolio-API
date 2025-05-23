from fastapi import FastAPI
from .database import Base, engine

from .routers import profile, skills, education, experience, visits

def create_db():
    Base.metadata.create_all(engine)

tags_metadata = [
    {
        "name": "Profile",
        "description": "Basic information about me",
        "externalDocs": {
            "description": "View my full profile",
            "url":"https://jacobarmstrong.dev"
        }
    },
    {
        "name": "Skills",
        "description": "Skills I've learned from school and taught myself"
    },
    {
        "name": "Education",
        "description": "History of my education"
    },
    {
        "name": "Experience",
        "description": "History of my work experience"
    },
    {
        "name": "Visits",
        "description": "**POST** a visit to my API! \nLeave your full name, relation (friend, family, recruiter, etc) and a message."
    }
]

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    description="Welcome to my Portfolio API!",
    contact = {
        "name": "Jacob Armstrong",
        "url": "https://jacobarmstrong.dev"
    },
    openapi_tags=tags_metadata
)

# Include routers
app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(visits.router)

@app.get("/")
async def root():
    return {
        "Introduction": "Welcome to my Portfolio! This is an interactive API to get more information about me, or leave a message saying you visted!",
        "Created by": "Jacob Armstrong",
        "Using": "FastAPI, Pydantic, SQLAlchemy and PostgreSQL",
        "Documentation": "api.jacobarmstrong.dev/docs"
    }

if __name__ == "__main__":
    create_db()