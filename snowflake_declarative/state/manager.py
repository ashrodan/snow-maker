from typing import Dict, List, Any
import yaml
import logging
import sys
from ..models.base import SnowflakeObject
from ..handlers.base import SnowflakeObjectHandler
from ..models.differences import ObjectDifference
from ..models.change_report import ChangeReport, ObjectChangeEntry, ChangeStatus

class SnowflakeState:
    """Manages the desired state of Snowflake objects"""
    
    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(self.__class__.__name__)
        self.handlers = {
            'database': DatabaseHandler(root),
            'warehouse': WarehouseHandler(root)
        }
        self.object_types = {
            'database': SnowflakeDatabase,
            'warehouse': SnowflakeWarehouse
        }

    def load_yaml_config(self, path: str) -> Dict[str, List[SnowflakeObject]]:
        """Load configurations from YAML"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        configs = {}
        for obj_type, obj_class in self.object_types.items():
            plural_type = f"{obj_type}s"
            if plural_type in data:
                configs[obj_type] = [obj_class(**obj) for obj in data[plural_type]]
        
        return configs

    def find_differences(self, desired: SnowflakeObject, actual: Any, 
                        handler: SnowflakeObjectHandler) -> List[ObjectDifference]:
        """Compare desired and actual states"""
        differences = []
        
        for field in handler.get_comparable_fields():
            desired_value = getattr(desired, field)
            actual_value = getattr(actual, field, None)

            if desired_value is None:
                continue

            if isinstance(desired_value, str):
                desired_value = desired_value.strip().upper()
            if isinstance(actual_value, str):
                actual_value = actual_value.strip().upper()

            if desired_value != actual_value:
                differences.append(ObjectDifference(
                    field=field,
                    expected=desired_value,
                    actual=actual_value
                ))

        return differences

    def apply_configuration(self, config_path: str, dry_run: bool = True) -> ChangeReport:
        """Apply configurations from YAML and generate a comprehensive change report"""
        # Initialize change report
        change_report = ChangeReport()
        
        # Load configurations
        configs = self.load_yaml_config(config_path)
        
        for obj_type, objects in configs.items():
            handler = self.handlers.get(obj_type)
            if not handler:
                self.logger.warning(f"No handler found for object type: {obj_type}")
                continue

            for obj in objects:
                try:
                    # Check if object exists
                    existing = handler.get_existing(obj.name)
                    
                    # Prepare change entry
                    change_entry = ObjectChangeEntry(
                        name=obj.name,
                        type=obj_type,
                        status=ChangeStatus.NO_CHANGE
                    )
                    
                    if not existing:
                        # Object does not exist, needs creation
                        change_entry.status = ChangeStatus.CREATED
                        if not dry_run:
                            handler.create(obj, dry_run)
                    else:
                        # Object exists, check for differences
                        differences = self.find_differences(obj, existing, handler)
                        
                        if differences:
                            # Object has differences
                            change_entry.status = ChangeStatus.UPDATED
                            change_entry.differences = differences
                            
                            self.logger.warning(
                                f"{obj_type.capitalize()} '{obj.name}' exists but has differences:"
                            )
                            for diff in differences:
                                self.logger.warning(f"  - {diff}")
                            
                            self.logger.warning(
                                f"Note: {obj_type.capitalize()} properties cannot be updated directly. "
                                f"You would need to recreate the {obj_type} to apply these changes."
                            )
                    
                    # Add change entry to report
                    change_report.add_change(obj_type, change_entry)

                except Exception as e:
                    # Handle any errors during processing
                    error_entry = ObjectChangeEntry(
                        name=obj.name,
                        type=obj_type,
                        status=ChangeStatus.ERROR,
                        error=str(e)
                    )
                    change_report.add_change(obj_type, error_entry)
                    self.logger.error(f"Error processing {obj_type} '{obj.name}': {e}")
        
        # Log summary
        self.logger.info("Change Report Summary:")
        self.logger.info(change_report.summary())
        
        return change_report

# Import handlers at the end to avoid circular imports
from ..handlers.database import DatabaseHandler
from ..handlers.warehouse import WarehouseHandler
from ..models.database import SnowflakeDatabase
from ..models.warehouse import SnowflakeWarehouse
