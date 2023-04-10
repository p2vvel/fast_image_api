from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError


from ..schemas.tier import TierForm
from ..models import Tier




def create_tier(tier: TierForm, db: Session) -> Tier:
    new_tier = Tier(**tier.dict())
    try: 
        db.add(new_tier)
        db.commit()
        db.refresh(new_tier)
        return new_tier
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Tier '{tier.name}' already exists")
