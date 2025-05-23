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

# PUT (UPDATE)
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
class SkillBase(BaseModel):
    category: str
    name: str

# POST
# Same structure as base
class SkillCreate(SkillBase):
    pass

# GET
# Show ID, since category and name are not unique
class SkillResponse(SkillBase):
    id: int

# PUT (UPDATE)
# Must include ID to update, name and category are not unique
class SkillUpdate(SkillBase):
    category: Optional[str] = None
    name: Optional[str] = None

# ================================
# =          Education           =
# ================================

# Base model
class EducationBase(BaseModel):
    school: str
    degree: str
    major: str
    dates: str
    description: str

# POST
# Same structure as base
class EducationCreate(EducationBase):
    pass

# GET
# Show ID, since school name may not be unique
class EducationResponse(EducationBase):
    id: int

# PUT (UPDATE)
# Must include ID to update
class EducationUpdate(EducationBase):
    school: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    dates: Optional[str] = None
    description: Optional[str] = None

# ================================
# =          Experience          =
# ================================

# Base model
class ExperienceBase(BaseModel):
    company: str
    role: str
    dates: str
    description: str

# POST
# Same structure as base
class ExperienceCreate(ExperienceBase):
    pass

# GET
# Show ID, since company may not be unique (different roles)
class ExperienceResponse(ExperienceBase):
    id: int

# PUT (UPDATE)
# Must include ID to update
class ExperienceUpdate(ExperienceBase):
    company: Optional[str] = None
    role: Optional[str] = None
    dates: Optional[str] = None
    description: Optional[str] = None