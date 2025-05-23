from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Skills
from ..schemas import SkillCreate, SkillResponse, SkillUpdate

import os

router = APIRouter()

api_key = os.getenv("API_KEY")
header_scheme = APIKeyHeader(name="api_key")

# POST
@router.post("/skills", response_model=SkillCreate, tags="Skills")
def create_skill(
    skill: SkillCreate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):
    
    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find existing skill with same name and category
    existing_skill = db.query(Skills).filter(Skills.category == skill.category, Skills.name == skill.name).first()

    if existing_skill:
        raise HTTPException(status_code=409, detail=f"{skill.name} already exists in {skill.category}.")
    
    # Dump pydantic model into dictionary, unpack into keywords, format into SQLAlchemy model instance
    new_skill = Skills(**skill.model_dump())

    # Add and commit SQLAlchemy model instance
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill

# GET
@router.get("/skills", response_model=list[SkillResponse], tags="Skills")
def get_skills(
    category: str | None = Query(default=None, description="(optional) Filter by category"),
    name: str | None = Query(default=None, description="(optional) Search for specific skill"),
    db: Session = Depends(get_db)):

    # Query skills table
    skills = db.query(Skills)

    if category:
        category = category.lower().title()
        skills = skills.filter(Skills.category == category)
    if name:
        name = name.lower().title()
        skills = skills.filter(Skills.name == name)

    # Select all results
    skills = skills.all()

    if not skills:
        raise HTTPException(status_code=404, detail=f"No skills found matching the provided parameters.")

    return skills

# @router.get("/skills/{category}", response_model=list(SkillResponse), tags="Skills")
# def get_skills_by_category(
#     category: str,
#     name: str | None = Query(default=None, description="(optional) Search for specific skill"),
#     db: Session = Depends(get_db)):

#     # Query skills table
#     skills = db.query(Skills)

#     # Filter by category
#     skills = skills.filter(Skills.category == category)

#     if name:
#         skills = skills.filter(Skills.name == name)

#     # Select all results
#     skills = skills.all()

#     if not skills:
#         raise HTTPException(status_code=404, detail=f"No skills found matching provided the provided parameters.")
    
#     return skills

# PUT
@router.put("/skills/{id}", response_model=SkillUpdate, tags="Skills")
def update_skill(
    id: int, # Update by ID, since name and category are not unique
    skill_update: SkillUpdate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")

    # Find specified skill
    skill = db.query(Skills).filter(Skills.id == id).first()

    if not skill:
        raise HTTPException(status_code=404, detail=f"\"{skill_update.category}\" skill \"{skill_update.name}\" not found.")
    
    # Ensure a skill does not already exist with updated info
    existing_skill = db.query(Skills).filter(Skills.category == skill_update.category and Skills.name == skill_update.name).first()

    if existing_skill:
        raise HTTPException(status_code=409, detail=f"Could not update. {skill_update.name} already exists in {skill_update.category}.")

    # Update skill
    skill.category = skill_update.category
    skill.name = skill_update.name

    # Commit changes to db
    db.commit()
    db.refresh(skill)

    return skill

# DELETE
@router.delete("/skills/{id}", response_model=SkillResponse, tags="Skills")
def delete_skill(
    id: int,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")

    # Find skill with provided name
    skill = db.query(Skills).filter(Skills.id == id).first()

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill with id {id} not found.")
    
    # Delete skill
    db.delete(skill)
    db.commit()

    return skill