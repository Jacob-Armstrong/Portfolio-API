from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Education
from ..schemas import EducationCreate, EducationResponse, EducationUpdate
import os

router = APIRouter()

api_key = os.getenv("API_KEY")
header_scheme = APIKeyHeader(name="api_key")

@router.post("/education", response_model=EducationCreate, tags="Education")
def create_education(
    education: EducationCreate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find existing education with same school, degree and major
    # There may be multiple degrees from the same school, even multiple of the same degree type, 
    # but not both degree AND major
    # e.g. Bachelor of Science, Computer Science and Bachelor of Science, Data Science
    existing_education = db.query(Education).filter(
        Education.school == education.school, 
        Education.degree == education.degree, 
        Education.major == education.major).first()

    if existing_education:
        raise HTTPException(status_code=409, detail=f"{education.degree} in {education.major} already exists for {education.school}.")
    
    # Dump pydantic model into dictionary, unpack into keywords, format into SQLAlchemy model instance
    new_education = Education(**education.model_dump())

    # Add and commit SQLAlchemy model instance
    db.add(new_education)
    db.commit()
    db.refresh(new_education)

    return new_education

# GET
@router.get("/education", response_model=list[EducationResponse], tags="Education")
def get_education(
    school: str | None = Query(default=None, description="(optional) Filter by school"),
    degree: str | None = Query(default=None, description="(optional) Filter by degree"),
    major: str | None = Query(default=None, description="(optional) Filter by major"),
    description: str | None = Query(default=None, description="(optional) Search for keywords in descriptions"),
    db: Session = Depends(get_db)):

    # Query Education table
    education = db.query(Education)

    if school:
        school = school.lower().title()
        education = education.filter(Education.school.ilike(f"%{school}%"))
    if degree:
        degree = degree.lower().title()
        education = education.filter(Education.degree.ilike(f"%{degree}%"))
    if major:
        major = degree.lower().title()
        education = education.filter(Education.degree.ilike(f"%{major}%"))
    if description:
        education = education.filter(Education.description.ilike(f"%{description}%"))

    # Select all results
    education = education.order_by(Education.id.desc()).all()

    if not education:
        raise HTTPException(status_code=404, detail=f"No education found matching the provided parameters.")
    
    return education

# PUT
@router.put("/education/{id}", response_model=EducationUpdate, tags="Education")
def update_education(
    id: int, #  Update by ID
    education_update: EducationUpdate,
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find specified education
    education = db.query(Education).filter(Education.id == id).first()

    if not education:
        raise HTTPException(status_code=404, detail=f"Education with id {id} not found")

    # Update education
    if education_update.school:
        education.school = education_update.school
    if education_update.degree:
        education.degree = education_update.degree
    if education_update.major:
        education.major = education_update.major
    if education_update.dates:
        education.dates = education_update.dates
    if education_update.description:
        education.description = education_update.description
    
    # Commit changes to db
    db.commit()
    db.refresh(education)

    return education

# DELETE
@router.delete("/education/{id}", response_model=EducationResponse, tags="Education")
def delete_education(
    id: int, # Delete by ID
    key: str = Depends(header_scheme),
    db: Session = Depends(get_db)):

    if key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized API key.")
    
    # Find education with provided ID
    education = db.query(Education).filter(Education.id == id).first()

    if not education:
        raise HTTPException(status_code=404, detail=f"Education with id {id} not found.")

    # Delete education
    db.delete(education)
    db.commit()

    return education

    