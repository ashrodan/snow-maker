# snowflake_declarative/handlers/base.py
from abc import ABC, abstractmethod
from typing import Optional, Any, List
import logging

class SnowflakeObjectHandler(ABC):
    """Abstract base class for object handlers"""
    
    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_existing(self, name: str) -> Optional[Any]:
        """Get existing object by name"""
        pass

    @abstractmethod
    def create(self, obj: Any, dry_run: bool = True) -> None:
        """Create new object"""
        pass

    @abstractmethod
    def get_comparable_fields(self) -> List[str]:
        """Get list of fields that should be compared"""
        pass
