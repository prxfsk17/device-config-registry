from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.diff import diff_parameters
from app.models import Configuration, Device
from app.schemas import ConfigDiff, ConfigurationCreate, ConfigurationOut

router = APIRouter(prefix="/devices/{device_id}/configs", tags=["configurations"])


def _ensure_device_exists(db: Session, device_id: int) -> None:
    if db.get(Device, device_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")


def _get_config_or_404(db: Session, device_id: int, version: int) -> Configuration:
    config = db.scalar(
        select(Configuration).where(
            Configuration.device_id == device_id,
            Configuration.version == version,
        )
    )
    if config is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Configuration version {version} not found")
    return config


@router.post("", response_model=ConfigurationOut, status_code=status.HTTP_201_CREATED)
def create_configuration(device_id: int, data: ConfigurationCreate, db: Session = Depends(get_db)):
    """Saves a new version of the configuration. Versions are numbered 1, 2, 3... per device."""
    _ensure_device_exists(db, device_id)

    last_version = db.scalar(
        select(func.max(Configuration.version)).where(Configuration.device_id == device_id)
    )
    config = Configuration(
        device_id=device_id,
        version=(last_version or 0) + 1,
        parameters=data.parameters,
        comment=data.comment,
    )
    db.add(config)
    try:
        db.commit()
    except IntegrityError:
        # Two requests tried to create the same version at the same moment.
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Version conflict, please retry")
    db.refresh(config)
    return config


@router.get("", response_model=list[ConfigurationOut])
def list_configurations(device_id: int, db: Session = Depends(get_db)):
    _ensure_device_exists(db, device_id)
    return db.scalars(
        select(Configuration)
        .where(Configuration.device_id == device_id)
        .order_by(Configuration.version)
    ).all()


# Fixed paths ("/latest", "/diff") must be declared before "/{version}".
@router.get("/latest", response_model=ConfigurationOut)
def get_latest_configuration(device_id: int, db: Session = Depends(get_db)):
    _ensure_device_exists(db, device_id)
    config = db.scalar(
        select(Configuration)
        .where(Configuration.device_id == device_id)
        .order_by(Configuration.version.desc())
        .limit(1)
    )
    if config is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This device has no configurations yet")
    return config


@router.get("/diff", response_model=ConfigDiff)
def diff_configurations(
    device_id: int,
    from_version: int,
    to_version: int,
    db: Session = Depends(get_db),
):
    """Shows what was added, removed or changed between two versions."""
    _ensure_device_exists(db, device_id)
    old = _get_config_or_404(db, device_id, from_version)
    new = _get_config_or_404(db, device_id, to_version)
    return ConfigDiff(
        from_version=from_version,
        to_version=to_version,
        **diff_parameters(old.parameters, new.parameters),
    )


@router.get("/{version}", response_model=ConfigurationOut)
def get_configuration(device_id: int, version: int, db: Session = Depends(get_db)):
    _ensure_device_exists(db, device_id)
    return _get_config_or_404(db, device_id, version)
