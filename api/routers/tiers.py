from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import tier as tier_crud
from ..dependencies.auth import get_admin_or_401

router = APIRouter(dependencies=[Depends(get_admin_or_401)])


@router.post("/")
def create_tier(tier: schemas.TierForm, db: Session = Depends(get_db)) -> schemas.TierResponse:
    new_tier = tier_crud.create_tier(tier, db)
    return new_tier


@router.get("/")
def get_all_tiers(db: Session = Depends(get_db)) -> list[schemas.TierResponse]:
    all_tiers = tier_crud.get_all_tiers(db)
    return all_tiers
    

@router.get("/{tier_name}")
def get_tier(tier_name: str, db: Session = Depends(get_db)) -> schemas.TierResponse:
    tier = tier_crud.get_tier_by_name(tier_name, db)
    return tier


@router.delete("/{tier_name}")
def delete_tier(tier_name: str, db: Session = Depends(get_db)) -> None:
    tier_crud.delete_tier_by_name(tier_name, db)
    raise HTTPException(status_code=status.HTTP_200_OK)
