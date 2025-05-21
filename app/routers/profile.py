from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db

from ..models import Profile
from ..schemas import ProfileCreate, ProfileResponse, ProfileUpdate

router = APIRouter()

# TODO: Require authorization on all methods except GET

# POST
@router.post("/profile", response_model=ProfileResponse, tags="Profile")
def create_profile(
    profile: ProfileCreate, 
    db: Session = Depends(get_db)):
    
    # Find profile with same name
    existing_profile = db.query(Profile).filter(Profile.name == profile.name).first()

    if existing_profile:
        raise HTTPException(status_code=409, detail=f"A profile for {profile.name} already exists.")
    
    # Dump pydantic model into dictionary, unpack into keywords, format into SQLAlchemy model instance
    new_profile = Profile(**profile.model_dump())

    # Add and commit SQLAlchemy model instance
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

# GET
@router.get("/profile", response_model=ProfileResponse, tags="Profile")
def get_profile(
    db: Session = Depends(get_db)):
    
    # Query profile table
    profile = db.query(Profile)

    # Select all results
    profile = profile.first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile is unavailable.")

    return profile

# PUT (Update)
@router.put("/profile/{name}", response_model=ProfileUpdate, tags="Profile")
def update_profile(
    name: str, # Must include name in query
    profile_update: ProfileUpdate, # Schema components to update
    db: Session = Depends(get_db)):

    # Find profile with provided name
    profile = db.query(Profile).filter(Profile.name == name).first()

    if not profile:
        raise HTTPException(status_code=404, detail=f"No profile found for {name}.")

    # If update includes parameters, replace them in db instance
    if profile_update.age:
        profile.age = profile_update.age
    if profile_update.about:
        profile.about = profile_update.about
    if profile_update.favorite_color:
        profile.favorite_color = profile_update.favorite_color
    if profile_update.favorite_food:
        profile.favorite_food = profile_update.favorite_food
    
    db.commit()
    db.refresh(profile)

    return profile

# DELETE
@router.delete("/profile/{name}", response_model=ProfileResponse, tags="Profile")
def delete_profile(
    name: str, # Name of profile to delete
    db: Session = Depends(get_db)):

    # Find profile with provided name
    profile = db.query(Profile).filter(Profile.name == name).first()

    if not profile:
        raise HTTPException(status_code=404, detail=f"No profile found for {name}.")
    
    db.delete(profile)
    db.commit()

    return profile