from datetime import datetime
from enum import Enum
import logging
from typing import Optional, List, Any
from pydantic import BaseModel, Field, validator, field_validator
from snowflake.core import CreateMode
import yaml

class DatabaseKind(str, Enum):
    PERMANENT = "PERMANENT"
    TEMPORARY = "TEMPORARY"
    TRANSIENT = "TRANSIENT"

class LogLevel(str, Enum):
    OFF = "OFF"
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"

class TraceLevel(str, Enum):
    OFF = "OFF"
    BASIC = "BASIC"
    VERBOSE = "VERBOSE"

class WarehouseSize(str, Enum):
    XSMALL = "X-SMALL"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    XLARGE = "X-LARGE"
    XXLARGE = "2X-LARGE"
    XXXLARGE = "3X-LARGE"
    X4LARGE = "4X-LARGE"

class CollationType(str, Enum):
    UTF8 = "UTF8"
    UTF8_CI = "UTF8_CI"
    UTF8_CS = "UTF8_CS"
    UTF8_BIN = "UTF8_BIN"

class SnowflakeDatabase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1,
        max_length=255,
        pattern="^[A-Za-z][A-Za-z0-9_]*$",
        description="Database name - must start with letter and contain only letters, numbers, and underscores"
    )
    created_on: Optional[datetime] = None
    kind: Optional[DatabaseKind] = Field(default=DatabaseKind.PERMANENT)
    is_default: Optional[bool] = None
    is_current: Optional[bool] = None
    origin: Optional[str] = None
    owner: Optional[str] = None
    comment: Optional[str] = Field(default=None, max_length=1000)
    options: Optional[str] = None
    retention_time: Optional[int] = Field(default=None, ge=0, le=90)
    dropped_on: Optional[datetime] = None
    budget: Optional[str] = Field(default=None, pattern="^[A-Za-z0-9_-]*$")
    owner_role_type: Optional[str] = None
    data_retention_time_in_days: Optional[int] = Field(default=None, ge=0, le=90)
    default_ddl_collation: Optional[CollationType] = None
    log_level: Optional[LogLevel] = None
    max_data_extension_time_in_days: Optional[int] = Field(default=None, ge=0, le=90)
    suspend_task_after_num_failures: Optional[int] = Field(default=None, ge=0, le=100)
    trace_level: Optional[TraceLevel] = None
    user_task_managed_initial_warehouse_size: Optional[WarehouseSize] = None
    user_task_timeout_ms: Optional[int] = Field(
        default=None,
        ge=0,
        le=86400000  # 24 hours in milliseconds
    )

    @validator('name')
    def validate_name(cls, v):
        reserved_words = {
            'DATABASE', 'TABLE', 'SCHEMA', 'VIEW', 'PROCEDURE', 'FUNCTION',
            'TRIGGER', 'SEQUENCE', 'STAGE', 'PIPE', 'TASK', 'STREAM',
            'TAG', 'SHARE', 'ROLE', 'USER', 'WAREHOUSE', 'ACCOUNT'
        }
        if v.upper() in reserved_words:
            raise ValueError(f'Name cannot be a reserved word: {v}')
        return v.upper()  # Snowflake identifiers are case-insensitive and stored in upper case

    @validator('data_retention_time_in_days')
    def validate_retention_time(cls, v, values):
        if v is not None and values.get('kind') == DatabaseKind.TEMPORARY:
            raise ValueError('Temporary databases cannot have retention time')
        return v

    @field_validator('default_ddl_collation', mode='before')
    def validate_collation(cls, v: Any) -> Optional[str]:
        if v is None or v == '' or v == 'None' or v == 'NONE':
            return None
        if isinstance(v, str):
            v = v.strip().upper()
            if v in CollationType._member_names_:
                return v
            return None
        return v

    class Config:
        from_attributes = True
        use_enum_values = True  # This ensures enum values are used instead of enum objects
        json_schema_extra = {
            "example": {
                "name": "MY_DATABASE",
                "kind": "PERMANENT",
                "comment": "Production database for analytics",
                "data_retention_time_in_days": 30,
                "log_level": "INFO",
                "default_ddl_collation": "UTF8",
                "user_task_managed_initial_warehouse_size": "X-SMALL",
                "user_task_timeout_ms": 3600000
            }
        }

    def to_snowflake_database(self) -> 'Database':
        """Convert Pydantic model to Snowflake Database object"""
        from snowflake.core.database import Database
        return Database(**self.model_dump(exclude_none=True))

    @classmethod
    def from_snowflake_database(cls, db: 'Database') -> 'SnowflakeDatabase':
        """Create Pydantic model from Snowflake Database object"""
        return cls.model_validate(db)

def create_database(root, db_config: SnowflakeDatabase):
    """Create a new database using Pydantic model"""
    snowflake_db = db_config.to_snowflake_database()
    return root.databases.create(snowflake_db)

def list_databases(root) -> List[SnowflakeDatabase]:
    """List all databases and return as Pydantic models"""
    databases = []
    for db in root.databases.iter():
        # Convert Snowflake Database object to dict and create Pydantic model
        db_model = SnowflakeDatabase.model_validate(db)
        databases.append(db_model)
    return databases

class DatabaseDifference(BaseModel):
    field: str
    expected: Any
    actual: Any

    def __str__(self):
        return f"{self.field}: expected '{self.expected}', got '{self.actual}'"

class SnowflakeState:
    """Manages the desired state of Snowflake databases"""
    
    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_yaml_config(self, path: str) -> List[SnowflakeDatabase]:
        """Load database configurations from YAML"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return [SnowflakeDatabase(**db) for db in data.get('databases', [])]

    def find_differences(self, desired: SnowflakeDatabase, actual: Any) -> List[DatabaseDifference]:
        """Compare desired and actual database states"""
        differences = []
        
        # Fields to compare
        comparable_fields = [
            'comment', 'kind', 'retention_time', 'budget',
            'data_retention_time_in_days', 'default_ddl_collation',
            'log_level', 'max_data_extension_time_in_days',
            'suspend_task_after_num_failures', 'trace_level',
            'user_task_managed_initial_warehouse_size',
            'user_task_timeout_ms'
        ]

        for field in comparable_fields:
            desired_value = getattr(desired, field)
            actual_value = getattr(actual, field, None)

            # Skip comparison if desired value is None (not specified)
            if desired_value is None:
                continue

            # Convert values to comparable format
            if isinstance(desired_value, str):
                desired_value = desired_value.strip().upper()
            if isinstance(actual_value, str):
                actual_value = actual_value.strip().upper()

            if desired_value != actual_value:
                differences.append(DatabaseDifference(
                    field=field,
                    expected=desired_value,
                    actual=actual_value
                ))

        return differences

    def apply_configuration(self, config_path: str, dry_run: bool = True) -> None:
        """Apply database configurations from YAML"""
        desired_databases = self.load_yaml_config(config_path)
        print(desired_databases)
        
        for desired_db in desired_databases:
            try:
                # Check if database exists
                existing_dbs = list(self.root.databases.iter(like=desired_db.name))
                print(len(existing_dbs) == 0)
                
                if len(existing_dbs) == 0:
                    self.logger.info(f"Database '{desired_db.name}' does not exist. Will create.")
                    if not dry_run:
                        from snowflake.core.database import Database
                        db = Database(**desired_db.model_dump(exclude_none=True))
                        self.root.databases.create(
                            db,
                            mode=CreateMode.if_not_exists
                        )
                        self.logger.info(f"Created database '{desired_db.name}'")
                else:
                    existing_db = existing_dbs[0]
                    differences = self.find_differences(desired_db, existing_db)
                    
                    if differences:
                        self.logger.warning(
                            f"Database '{desired_db.name}' exists but has differences:"
                        )
                        for diff in differences:
                            self.logger.warning(f"  - {diff}")
                        self.logger.warning(
                            "Note: Database properties cannot be updated directly. "
                            "You would need to recreate the database to apply these changes."
                        )
                    else:
                        self.logger.info(f"Database '{desired_db.name}' exists and matches desired state.")

            except Exception as e:
                self.logger.error(f"Error processing database '{desired_db.name}': {e}")
