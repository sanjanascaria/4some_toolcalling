from pydantic import BaseModel
from typing import List, Optional

class UserUpdate(BaseModel):
    personality_type: str
    age_range: str
    interest: str
    location: str
    willing_to_travel: str
    gender_pref: str

class UserCreate(UserUpdate):
    id: int

class UserRead(UserUpdate):
    id: int

class Feedback(BaseModel):
    session_id: str
    user_input: str