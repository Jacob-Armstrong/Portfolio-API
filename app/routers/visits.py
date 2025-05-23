from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..database import get_db

from pytz import timezone
import pytz
from datetime import datetime

from ..models import Visits
from ..schemas import VisitCreate, VisitResponse, VisitUpdate
import os

router = APIRouter()

api_key = os.getenv("API_KEY")
header_scheme = APIKeyHeader(name="api_key")

# POST
@router.post("/visits", response_model=VisitCreate, tags="Visits")
def create_visit(
    visit: VisitCreate,
    # No API key required to visit!
    db: Session = Depends(get_db)):

    # Find EXACT duplicate entry (same name, relation AND message)
    existing_visit = db.query(Visits).filter(
        Visits.name == visit.name,
        Visits.relation == visit.relation,
        Visits.message == visit.message).first()
    
    if existing_visit:
        raise HTTPException(status_code=404, detail=f"{visit.name} already has a visit with the message '{visit.message}'.")

    # Dump pydantic model into dictionary, unpack into keywords, format into SQLAlchemy model instance
    new_visit = Visits(**visit.model_dump(exclude="date"))

    # Add and commit SQLAlchemy model instance
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)

    return new_visit

# GET
@router.get("/visits", response_model=list[VisitResponse], tags="Visits")
def get_visits(
    name: str | None = Query(default=None, description="(optional) Filter by name"),
    relation: str | None = Query(default=None, description="(optional) Filter by relation"),
    message: str | None = Query(default=None, description="(optional) Search for keywords in messages"),
    db: Session = Depends(get_db)):

    # Query visits table
    visits = db.query(Visits)

    if name:
        visits = visits.filter(Visits.name.ilike(f"%{name}%"))
    if relation:
        visits = visits.filter(Visits.relation.ilike(f"%{relation}%"))
    if message:
        visits = visits.filter(Visits.message.ilike(f"%{message}%"))

    # Select all results
    visits = visits.order_by(Visits.id.desc()).all()

    if not visits:
        raise HTTPException(status_code=404, detail=f"No visits found matching the provided parameters.")
    
    # Convert timezones to Pacific (they are stored as UTC)
    pacific = timezone("America/Los_Angeles")
    for visit in visits:
        visit.date = visit.date.astimezone(pacific).strftime("%m-%d-%Y %I:%M%p %Z")

    return visits

