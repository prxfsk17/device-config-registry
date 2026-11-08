from datetime import datetime

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
