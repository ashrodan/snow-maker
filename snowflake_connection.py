import os
import argparse
import sys
from dotenv import load_dotenv

# Dynamically import Snowflake package
try:
    import snowflake
    from snowflake.core import Root
    from snowflake.core.session import Session
except ImportError:
    print("Error: Please install the Snowflake package using 'pip install snowflake'")
    raise

def load_env_config(env='dev'):
    """
    Load environment-specific configuration.
    
    :param env: Environment ('dev', 'tst', or 'prd')
    :return: Path to the environment-specific .env file
    """
    # Prioritize environment-specific .env files in config/
    env_file = f'config/{env}/.env'
    
    # Fallback to root .env files with environment suffix
    if not os.path.exists(env_file):
        env_file = f'.env.{env}'
    
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Configuration file not found: {env_file}")
    
    load_dotenv(env_file)
    return env_file

def get_connection_parameters(env='dev'):
    """
    Retrieve Snowflake connection parameters from environment variables.
    
    :param env: Environment to load configuration for
    :return: Dictionary of connection parameters
    """
    # Load the specific environment configuration
    load_env_config(env)
    
    connection_parameters = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'database': os.getenv('SNOWFLAKE_DATABASE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE')
    }
    
    # Remove None values and validate required parameters
    connection_parameters = {k: v for k, v in connection_parameters.items() if v is not None}
    
    if not all(key in connection_parameters for key in ['account', 'user', 'password']):
        raise ValueError("Missing required Snowflake connection parameters")
    
    return connection_parameters

def create_snowflake_session(env='dev'):
    """
    Create a Snowflake session using connection parameters.
    
    :param env: Environment to connect to
    :return: Snowflake Session object
    """
    try:
        # Get connection parameters
        connection_parameters = get_connection_parameters(env)
        
        # Create session using Session.builder
        session = Session.builder.configs(connection_parameters).create()
        
        print(f"Successfully created Snowflake session for {env.upper()} environment")
        return session
    
    except Exception as e:
        print(f"Error creating Snowflake session: {e}")
        raise

def get_snowflake_root(session):
    """
    Create the root resource for Snowflake API interactions.
    
    :param session: Snowflake Session object
    :return: Root resource
    """
    try:
        root = Root(session)
        print("Successfully created Snowflake Root resource")
        return root
    
    except Exception as e:
        print(f"Error creating Snowflake Root resource: {e}")
        raise

def parse_arguments():
    """
    Parse command-line arguments.
    
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Snowflake Connection Script')
    parser.add_argument('-e', '--env', 
                        choices=['dev', 'tst', 'prd'], 
                        default='dev', 
                        help='Environment to connect to (default: dev)')
    parser.add_argument('-l', '--list-databases', 
                        action='store_true', 
                        help='List available databases')
    
    return parser.parse_args()

def main():
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Create Snowflake session
        session = create_snowflake_session(args.env)
        
        # Create root resource
        root = get_snowflake_root(session)
        
        # Optional: List databases if requested
        if args.list_databases:
            try:
                databases = root.databases.list()
                print("\nAvailable Databases:")
                for db in databases:
                    print(f"- {db.name}")
            except Exception as e:
                print(f"Error listing databases: {e}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Close the session if it exists
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
