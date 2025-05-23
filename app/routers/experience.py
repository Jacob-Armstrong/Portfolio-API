from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Experience
from ..schemas import ExperienceCreate, ExperienceResponse, ExperienceUpdate
import os

router = APIRouter()

api_key = os.getenv("API_KEY")
header_scheme = APIKeyHeader(name="api_key")

# POST
@router.post("/experience", response_model=ExperienceCreate, tags=["Experience"])
def create_experience(
    experience: ExperienceCreate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")

    # Find existing experience with same company and role
    existing_experience = db.query(Experience).filter(
        Experience.company == experience.company, 
        Experience.role == experience.role).first()
    
    if existing_experience:
        raise HTTPException(status_code=409, detail=f"{experience.role} already exists for {experience.company}.")
    
    # Dump pydantic model into dictionary, unpack into keywords, format into SQLAlchemy model instance
    new_experience = Experience(**experience.model_dump())

    # Add and commit SQLAlchemy model instance
    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)

    return new_experience

# GET
@router.get("/experience", response_model=list[ExperienceResponse], tags=["Experience"])
def get_experience(
    company: str | None = Query(default=None, description="(optional) Filter by company"),
    role: str | None = Query(default=None, description="(optional) Filter by role"),
    description: str | None = Query(default=None, description="(optional) Search for keywords in descriptions"),
    db: Session = Depends(get_db)):

    # Query experience table
    experience = db.query(Experience)

    if company:
        company = company.lower().title()
        experience = experience.filter(Experience.company.ilike(f"%{company}%"))
    if role:
        role = role.lower().title()
        experience = experience.filter(Experience.role.ilike(f"%{role}%"))
    if description:
        experience = experience.filter(Experience.description.ilike(f"%{description}%"))
    
    # Select all results
    experience = experience.order_by(Experience.id.desc()).all()

    if not experience:
        raise HTTPException(status_code=404, detail=f"No experience found matching the provided parameters.")
    
    return experience

# PUT
@router.put("/experience/{id}", response_model=ExperienceUpdate, tags=["Experience"])
def update_experience(
    id: int, # Update by ID
    experience_update: ExperienceUpdate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find specified experience
    experience = db.query(Experience).filter(Experience.id == id).first()

    if not experience:
        raise HTTPException(status_code=404, detail=f"Experience with id {id} not found.")
    
    # Update experience
    if experience_update.company:
        experience.company = experience_update.company
    if experience_update.role:
        experience.role = experience_update.role
    if experience_update.dates:
        experience.dates = experience_update.dates
    if experience_update.description:
        experience.description = experience_update.description
    
    # Commit changes to db
    db.commit()
    db.refresh(experience)

    return experience

# DELETE
@router.delete("/experience/{id}", response_model=ExperienceResponse, tags=["Experience"])
def delete_experience(
    id: int, # Delete by ID
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find experience with provided ID
    experience = db.query(Experience).filter(Experience.id == id).first()

    if not experience:
        raise HTTPException(status_code=404, detail=f"Experience with id {id} not found.")
    
    # Delete experience
    db.delete(experience)
    db.commit()

    return experience