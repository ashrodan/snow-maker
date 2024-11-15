from typing import Optional, Any, List
from .base import SnowflakeObjectHandler
from ..models.warehouse import SnowflakeWarehouse

class WarehouseHandler(SnowflakeObjectHandler):
    def get_existing(self, name: str) -> Optional[Any]:
        try:
            warehouses = list(self.root.warehouses.iter(like=name))
            return warehouses[0] if warehouses else None
        except Exception as e:
            self.logger.error(f"Error getting warehouse {name}: {e}")
            return None

    def create(self, obj: SnowflakeWarehouse, dry_run: bool = True) -> None:
        if not dry_run:
            from snowflake.core.warehouse import Warehouse
            wh = Warehouse(**obj.model_dump(exclude_none=True))
            self.root.warehouses.create(wh)
            self.logger.info(f"Created warehouse '{obj.name}'")
        else:
            self.logger.info(f"Would create warehouse '{obj.name}'")

    def get_comparable_fields(self) -> List[str]:
        return ['size', 'auto_suspend', 'auto_resume', 'comment']
