from fastapi import Depends, APIRouter
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
