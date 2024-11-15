from typing import Optional
from pydantic import Field
from .base import SnowflakeObject

class SnowflakeWarehouse(SnowflakeObject):
    """Warehouse specific configuration"""
    size: str = Field(default="X-SMALL")
    auto_suspend: Optional[int] = None
    auto_resume: bool = True
    comment: Optional[str] = None
