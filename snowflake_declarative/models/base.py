# snowflake_declarative/models/base.py
from pydantic import BaseModel, Field
from typing import Optional

class SnowflakeObject(BaseModel):
    """Base class for all Snowflake objects"""
    name: str = Field(..., pattern="^[A-Za-z][A-Za-z0-9_]*$")

    @property
    def object_type(self) -> str:
        return self.__class__.__name__.replace('Snowflake', '').lower()

    class Config:
        from_attributes = True
