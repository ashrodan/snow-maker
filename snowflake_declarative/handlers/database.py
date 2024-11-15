from typing import Optional, Any, List
from .base import SnowflakeObjectHandler
from ..models.database import SnowflakeDatabase

class DatabaseHandler(SnowflakeObjectHandler):
    def get_existing(self, name: str) -> Optional[Any]:
        try:
            dbs = list(self.root.databases.iter(like=name))
            return dbs[0] if dbs else None
        except Exception as e:
            self.logger.error(f"Error getting database {name}: {e}")
            return None

    def create(self, obj: SnowflakeDatabase, dry_run: bool = True) -> None:
        if not dry_run:
            from snowflake.core.database import Database
            from snowflake.core import CreateMode
            db = Database(**obj.model_dump(exclude_none=True))
            self.root.databases.create(db, mode=CreateMode.if_not_exists)
            self.logger.info(f"Created database '{obj.name}'")
        else:
            self.logger.info(f"Would create database '{obj.name}'")

    def get_comparable_fields(self) -> List[str]:
        return [
            'comment', 'kind', 'retention_time', 'budget',
            'data_retention_time_in_days', 'default_ddl_collation',
            'log_level', 'max_data_extension_time_in_days',
            'suspend_task_after_num_failures', 'trace_level',
            'user_task_managed_initial_warehouse_size',
            'user_task_timeout_ms'
        ]
