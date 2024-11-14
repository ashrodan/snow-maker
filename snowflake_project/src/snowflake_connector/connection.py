import os
from typing import Dict, List, Any
import snowflake.connector
from snowflake.core import Root
from snowflake.core.session import Session

class SnowflakeConnector:
    """
    A comprehensive Snowflake connection management class.
    """
    def __init__(self, config: Dict[str, str]):
        """
        Initialize the Snowflake connector with configuration.
        
        :param config: Dictionary of Snowflake connection parameters
        """
        self._config = config
        self._session = None
        self._root = None
    
    def create_session(self) -> Session:
        """
        Create a Snowflake session using the provided configuration.
        
        :return: Snowflake Session object
        """
        try:
            # Validate required parameters
            required_params = ['account', 'user', 'password']
            for param in required_params:
                if param not in self._config:
                    raise ValueError(f"Missing required parameter: {param}")
            
            # Create session
            self._session = Session.builder.configs(self._config).create()
            
            # Create root resource
            self._root = Root(self._session)
            
            print("Successfully created Snowflake session")
            return self._session
        
        except Exception as e:
            print(f"Error creating Snowflake session: {e}")
            raise
    
    def list_databases(self) -> List[str]:
        """
        List available databases in the Snowflake account.
        
        :return: List of database names
        """
        if not self._root:
            raise RuntimeError("Session not established. Call create_session() first.")
        
        try:
            databases = self._root.databases.list()
            return [db.name for db in databases]
        except Exception as e:
            print(f"Error listing databases: {e}")
            raise
    
    def execute_query(self, query: str) -> List[Any]:
        """
        Execute a SQL query and return results.
        
        :param query: SQL query to execute
        :return: List of query results
        """
        if not self._session:
            raise RuntimeError("Session not established. Call create_session() first.")
        
        try:
            cursor = self._session.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
    
    def close_session(self):
        """
        Close the current Snowflake session.
        """
        if self._session:
            try:
                self._session.close()
                print("Snowflake session closed")
            except Exception as e:
                print(f"Error closing session: {e}")
            finally:
                self._session = None
                self._root = None
