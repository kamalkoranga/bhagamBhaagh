from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.profile.schemas import ProfileOut

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])

@router.get("", response_model=ProfileOut)
def get_profile(current_user: User = Depends(get_current_user)) -> ProfileOut:
    return ProfileOut.model_validate(
        current_user,
        from_attributes=True
    )
