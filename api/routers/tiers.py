from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import tier as tier_crud
from ..dependencies.auth import get_admin_or_401, get_user_or_401
from ..models import User


router = APIRouter()


@router.post("/", dependencies=[Depends(get_admin_or_401)])
def create_tier(
    tier: schemas.TierForm, db: Session = Depends(get_db)
) -> schemas.TierResponseAdmin:
    new_tier = tier_crud.create_tier(tier, db)
    return new_tier


@router.get("/")
def get_all_tiers(
    db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> list[schemas.TierResponseAdmin | schemas.TierResponseStandard]:
    all_tiers = tier_crud.get_all_tiers(db)
    if user.is_superuser:
        return [schemas.TierResponseAdmin(**k.__dict__) for k in all_tiers]
    else:
        return [schemas.TierResponseStandard(**k.__dict__) for k in all_tiers]


@router.get("/{tier_name}")
def get_tier(
    tier_name: str, db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> schemas.TierResponseAdmin | schemas.TierResponseStandard:
    tier = tier_crud.get_tier_by_name(tier_name, db)
    if user.is_superuser:
        return schemas.TierResponseAdmin(**tier.__dict__)
    else:
        return schemas.TierResponseStandard(**tier.__dict__)


@router.delete("/{tier_name}", dependencies=[Depends(get_admin_or_401)])
def delete_tier(tier_name: str, db: Session = Depends(get_db)) -> None:
    tier_crud.delete_tier_by_name(tier_name, db)
    raise HTTPException(status_code=status.HTTP_200_OK)
