from typing import Dict, List, Optional, Any
from enum import Enum, auto
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from .differences import ObjectDifference

class ChangeStatus(str, Enum):
    """Enum representing the status of a change"""
    NO_CHANGE = "NO_CHANGE"
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    ERROR = "ERROR"

class ObjectChangeEntry(BaseModel):
    """Detailed change information for a specific object"""
    name: str
    type: str
    status: ChangeStatus
    differences: Optional[List[ObjectDifference]] = None
    error: Optional[str] = None

    model_config = ConfigDict(
        json_encoders={
            ChangeStatus: lambda v: v.value
        }
    )

class ChangeReport(BaseModel):
    """Comprehensive report of changes across Snowflake objects"""
    total_objects: int = 0
    objects_processed: int = 0
    objects_created: int = 0
    objects_updated: int = 0
    objects_no_change: int = 0
    objects_with_errors: int = 0
    
    changes: Dict[str, List[ObjectChangeEntry]] = Field(default_factory=dict)
    
    def add_change(self, object_type: str, change_entry: ObjectChangeEntry):
        """Add a change entry to the report"""
        if object_type not in self.changes:
            self.changes[object_type] = []
        
        self.changes[object_type].append(change_entry)
        
        # Update summary statistics
        self.total_objects += 1
        self.objects_processed += 1
        
        if change_entry.status == ChangeStatus.CREATED:
            self.objects_created += 1
        elif change_entry.status == ChangeStatus.UPDATED:
            self.objects_updated += 1
        elif change_entry.status == ChangeStatus.NO_CHANGE:
            self.objects_no_change += 1
        elif change_entry.status == ChangeStatus.ERROR:
            self.objects_with_errors += 1
    
    def summary(self) -> str:
        """Generate a human-readable summary of changes"""
        summary_lines = [
            f"Total Objects: {self.total_objects}",
            f"Objects Processed: {self.objects_processed}",
            f"Objects Created: {self.objects_created}",
            f"Objects Updated: {self.objects_updated}",
            f"Objects with No Changes: {self.objects_no_change}",
            f"Objects with Errors: {self.objects_with_errors}"
        ]
        return "\n".join(summary_lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the change report to a dictionary for serialization"""
        return {
            "total_objects": self.total_objects,
            "objects_processed": self.objects_processed,
            "objects_created": self.objects_created,
            "objects_updated": self.objects_updated,
            "objects_no_change": self.objects_no_change,
            "objects_with_errors": self.objects_with_errors,
            "changes": {
                obj_type: [entry.model_dump() for entry in entries]
                for obj_type, entries in self.changes.items()
            }
        }
