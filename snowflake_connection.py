import os
import argparse
import sys
import logging
import json
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dynamically import Snowflake package
try:
    from snowflake.core import Root
    from snowflake.snowpark import Session
except ImportError:
    logger.error("Error: Please install the Snowflake package using 'pip install snowflake'")
    raise

# Import Snowflake Declarative components
from snowflake_declarative import SnowflakeState

def load_env_config(env='dev'):
    """Load environment-specific configuration"""
    env_file = f'config/{env}/.env'
    
    if not os.path.exists(env_file):
        env_file = f'.env.{env}'
    
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Configuration file not found: {env_file}")
    
    load_dotenv(env_file)
    return env_file

def get_connection_parameters(env='dev'):
    """Retrieve Snowflake connection parameters from environment variables"""
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
    
    connection_parameters = {k: v for k, v in connection_parameters.items() if v is not None}
    
    if not all(key in connection_parameters for key in ['account', 'user', 'password']):
        raise ValueError("Missing required Snowflake connection parameters")
    
    return connection_parameters

def create_snowflake_session(env='dev'):
    """Create a Snowflake session using connection parameters"""
    try:
        connection_parameters = get_connection_parameters(env)
        session = Session.builder.configs(connection_parameters).create()
        
        logger.info(f"Successfully created Snowflake session for {env.upper()} environment")
        return session
    
    except Exception as e:
        logger.error(f"Error creating Snowflake session: {e}")
        raise

def get_snowflake_root(session):
    """Create the root resource for Snowflake API interactions"""
    try:
        root = Root(session)
        logger.info("Successfully created Snowflake Root resource")
        return root
    
    except Exception as e:
        logger.error(f"Error creating Snowflake Root resource: {e}")
        raise

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Snowflake Connection Script')
    parser.add_argument('-e', '--env', 
                        choices=['dev', 'tst', 'prd'], 
                        default='dev', 
                        help='Environment to connect to (default: dev)')
    parser.add_argument('-c', '--config', 
                        default='config/base_config.yaml', 
                        help='Path to configuration file')
    parser.add_argument('--dry-run', 
                        action='store_true', 
                        help='Perform a dry run without making changes')
    parser.add_argument('--output', 
                        help='Export change report to a JSON file')
    
    return parser.parse_args()

def main():
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Create Snowflake session
        session = create_snowflake_session(args.env)
        
        # Create root resource
        root = get_snowflake_root(session)
        
        # Manage Snowflake objects and generate change report
        def manage_snowflake_objects(root, config_path: str, dry_run: bool = True):
            state_manager = SnowflakeState(root)
            logger.info(f"{'Dry run: ' if dry_run else ''}Applying Snowflake configurations...")
            change_report = state_manager.apply_configuration(config_path, dry_run=dry_run)
            return change_report

        # Generate change report
        change_report = manage_snowflake_objects(root, args.config, args.dry_run)
        
        # Export change report if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(change_report.to_dict(), f, indent=2)
            logger.info(f"Change report exported to {args.output}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Close the session if it exists
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
