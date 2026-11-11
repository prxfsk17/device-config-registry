from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DeviceTypeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class DeviceTypeOut(DeviceTypeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class DeviceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    device_type_id: int


class DeviceOut(DeviceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ConfigurationCreate(BaseModel):
    parameters: dict[str, Any] = Field(min_length=1)
    comment: str | None = None


class ConfigurationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: int
    version: int
    parameters: dict[str, Any]
    comment: str | None
    created_at: datetime


class ChangedValue(BaseModel):
    old: Any
    new: Any


class ConfigDiff(BaseModel):
    from_version: int
    to_version: int
    added: dict[str, Any]
    removed: dict[str, Any]
    changed: dict[str, ChangedValue]
