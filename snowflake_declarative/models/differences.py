from pydantic import BaseModel
from typing import Any

class ObjectDifference(BaseModel):
    field: str
    expected: Any
    actual: Any

    def __str__(self):
        return f"{self.field}: expected '{self.expected}', got '{self.actual}'"
