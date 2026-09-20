import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class ProfileOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    created_at: datetime


class ProfileStatsOut(BaseModel):
    total_distance_m: float
    total_territory_m2: float
    territory_count: int
    completed_run_count: int
