import os
from typing import Dict
from dotenv import load_dotenv

def load_env_config(env: str = 'dev') -> Dict[str, str]:
    """
    Load Snowflake connection parameters from environment-specific .env file.
    
    :param env: Environment to load configuration for ('dev', 'tst', 'prd')
    :return: Dictionary of connection parameters
    """
    # Determine the .env file path
    env_file = f'.env.{env}'
    
    # Load environment variables from the specific .env file
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Configuration file not found: {env_file}")
    
    load_dotenv(env_file)
    
    # Extract Snowflake connection parameters
    connection_parameters = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'database': os.getenv('SNOWFLAKE_DATABASE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE')
    }
    
    # Remove None values
    connection_parameters = {k: v for k, v in connection_parameters.items() if v is not None}
    
    # Validate required parameters
    required_params = ['account', 'user', 'password']
    for param in required_params:
        if param not in connection_parameters:
            raise ValueError(f"Missing required Snowflake connection parameter: {param}")
    
    return connection_parameters
