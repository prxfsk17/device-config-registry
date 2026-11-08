from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import DeviceType
from app.schemas import DeviceTypeCreate, DeviceTypeOut

router = APIRouter(prefix="/device-types", tags=["device types"])


@router.post("", response_model=DeviceTypeOut, status_code=status.HTTP_201_CREATED)
def create_device_type(data: DeviceTypeCreate, db: Session = Depends(get_db)):
    device_type = DeviceType(**data.model_dump())
    db.add(device_type)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Device type with this name already exists")
    db.refresh(device_type)
    return device_type


@router.get("", response_model=list[DeviceTypeOut])
def list_device_types(db: Session = Depends(get_db)):
    return db.scalars(select(DeviceType).order_by(DeviceType.id)).all()


@router.get("/{device_type_id}", response_model=DeviceTypeOut)
def get_device_type(device_type_id: int, db: Session = Depends(get_db)):
    device_type = db.get(DeviceType, device_type_id)
    if device_type is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device type not found")
    return device_type
