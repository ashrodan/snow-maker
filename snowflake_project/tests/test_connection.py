import pytest
import os
from src.snowflake_connector.connection import SnowflakeConnector
from src.snowflake_connector.utils.config_loader import load_env_config

class TestSnowflakeConnector:
    @pytest.fixture
    def sample_config(self):
        """
        Fixture to provide a sample configuration for testing.
        In a real scenario, use a test-specific .env file.
        """
        return {
            'account': os.getenv('SNOWFLAKE_ACCOUNT', 'test_account'),
            'user': os.getenv('SNOWFLAKE_USER', 'test_user'),
            'password': os.getenv('SNOWFLAKE_PASSWORD', 'test_password')
        }
    
    def test_config_loader(self):
        """
        Test the configuration loader utility.
        """
        try:
            # Attempt to load configuration for dev environment
            config = load_env_config('dev')
            
            # Check that required keys are present
            assert 'account' in config
            assert 'user' in config
            assert 'password' in config
        except Exception as e:
            pytest.fail(f"Configuration loading failed: {e}")
    
    def test_connection_initialization(self, sample_config):
        """
        Test Snowflake connector initialization.
        """
        try:
            connector = SnowflakeConnector(sample_config)
            assert connector is not None
        except Exception as e:
            pytest.fail(f"Connector initialization failed: {e}")
    
    def test_session_creation(self, sample_config):
        """
        Test Snowflake session creation.
        Note: This is a basic test and might require mocking in a real-world scenario.
        """
        connector = SnowflakeConnector(sample_config)
        
        try:
            session = connector.create_session()
            assert session is not None
        except Exception as e:
            pytest.fail(f"Session creation failed: {e}")
        finally:
            # Ensure session is closed
            connector.close_session()
    
    def test_query_execution(self, sample_config):
        """
        Test basic query execution.
        """
        connector = SnowflakeConnector(sample_config)
        
        try:
            connector.create_session()
            
            # Test a simple query
            results = connector.execute_query("SELECT CURRENT_VERSION()")
            
            assert results is not None
            assert len(results) > 0
        except Exception as e:
            pytest.fail(f"Query execution failed: {e}")
        finally:
            # Ensure session is closed
            connector.close_session()
