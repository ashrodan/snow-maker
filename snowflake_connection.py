import os
import argparse
import sys
import logging
from dotenv import load_dotenv
from snowflake_declarative import SnowflakeState
# from models.database import SnowflakeDatabase, SnowflakeState, list_databases

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to capture info and warning messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Add console output
    ]
)
logger = logging.getLogger(__name__)

# Dynamically import Snowflake package
try:
    # import snowflake
    from snowflake.core import Root
    from snowflake.snowpark import Session
except ImportError:
    logger.error("Error: Please install the Snowflake package using 'pip install snowflake'")
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
        
        logger.info(f"Successfully created Snowflake session for {env.upper()} environment")
        return session
    
    except Exception as e:
        logger.error(f"Error creating Snowflake session: {e}")
        raise

def get_snowflake_root(session):
    """
    Create the root resource for Snowflake API interactions.
    
    :param session: Snowflake Session object
    :return: Root resource
    """
    try:
        root = Root(session)
        logger.info("Successfully created Snowflake Root resource")

        return root
    
    except Exception as e:
        logger.error(f"Error creating Snowflake Root resource: {e}")
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
        
        from snowflake.core.database import Database
        databases = root.databases #['ONYX_POC'].database_roles
        # new_database = Database(
        #     name="my_new_database",
        #     comment="this is my new database to prototype a new feature in",
        #     )
        # databases.create(new_database)
        # List databases
        logger.info("Listing databases:")
        print(databases)
        for database in databases.iter():
            logger.info(f"Database: {database.name}, Comment: {database.comment}, Owner: {database.owner}")

        
        def manage_snowflake_objects(root, config_path: str, dry_run: bool = True):
            state_manager = SnowflakeState(root)
            logger.info(f"{'Dry run: ' if dry_run else ''}Applying Snowflake configurations...")
            state_manager.apply_configuration(config_path, dry_run=dry_run)

        manage_snowflake_objects(root, "config/base_config.yaml", dry_run=True)

        # Optional: List databases if requested
        if args.list_databases:
            try:
                databases = root.databases.list()
                logger.info("\nAvailable Databases:")
                for db in databases:
                    logger.info(f"- {db.name}")
            except Exception as e:
                logger.error(f"Error listing databases: {e}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Close the session if it exists
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
