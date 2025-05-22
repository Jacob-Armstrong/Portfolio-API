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
# Same structure as base
class ProfileResponse(ProfileBase):
    pass

# UPDATE
# Must include name in update -- other fields are optional
class ProfileUpdate(ProfileBase):
    age: Optional[int] = None
    about: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_food: Optional[str] = None

# ================================
# =            Skills            =
# ================================

# Base model
class SkillsBase(BaseModel):
    category: str
    name: str

# POST
# Same structure as base
class SkillsCreate(SkillsBase):
    pass

# GET
# Same structure as base
class SkillsResponse(SkillsBase):
    pass

# UPDATE
# Must include both values
class SkillsUpdate(SkillsBase):
    pass