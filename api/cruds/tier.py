from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import select

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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Tier '{tier.name}' already exists"
        )


def get_all_tiers(db: Session) -> list[Tier]:
    all_tiers = db.execute(select(Tier)).all()
    return all_tiers


def get_tier_by_name(tier_name: str, db: Session) -> Tier:
    try:
        query = select(Tier).filter(Tier.name == tier_name)
        tier = db.scalar(query)
        return tier
    except NoResultFound:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_tier_by_name(tier_name: str, db: Session) -> None:
    tier = get_tier_by_name(tier_name, db)
    db.delete(tier)
    db.commit()
