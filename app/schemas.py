from pydantic import BaseModel
from typing import List, Optional

# Structures for API interactions (validation)

# ================================
# =           Profile            =
# ================================

# Base model
class ProfileBase(BaseModel):
    name: str
    age: int
    about: str
    favorite_color: str
    favorite_food: str

# POST
# Same structure as base
class ProfileCreate(ProfileBase):
    pass

# GET
# Include generated ID in response
class ProfileResponse(ProfileBase):
    id: int

    class Config:
        orm_mode = True

# UPDATE
# Can update age, about, and favorites
class ProfileUpdate(ProfileBase):
    age: Optional[int] = None
    about: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_food: Optional[str] = None