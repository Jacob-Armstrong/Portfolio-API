from pydantic import BaseModel
from typing import List

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
class ProfileCreate(ProfileBase):
    pass

# GET
class ProfileResponse(ProfileBase):
    id: int

    class Config:
        orm_mode = True