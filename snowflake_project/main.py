import sys
import argparse
from src.snowflake_connector.connection import SnowflakeConnector
from src.snowflake_connector.utils.config_loader import load_env_config

def parse_arguments():
    """
    Parse command-line arguments for Snowflake operations.
    
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Snowflake Connector Project')
    parser.add_argument('-e', '--env', 
                        choices=['dev', 'tst', 'prd'], 
                        default='dev', 
                        help='Environment to connect to (default: dev)')
    parser.add_argument('-l', '--list-databases', 
                        action='store_true', 
                        help='List available databases')
    parser.add_argument('-q', '--query', 
                        type=str, 
                        help='Execute a specific SQL query')
    
    return parser.parse_args()

def main():
    """
    Main entry point for the Snowflake Connector application.
    """
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Load environment-specific configuration
        config = load_env_config(args.env)
        
        # Create Snowflake connector
        connector = SnowflakeConnector(config)
        
        # Establish connection
        session = connector.create_session()
        
        # Optional: List databases
        if args.list_databases:
            databases = connector.list_databases()
            print("\nAvailable Databases:")
            for db in databases:
                print(f"- {db}")
        
        # Optional: Execute custom query
        if args.query:
            results = connector.execute_query(args.query)
            print("\nQuery Results:")
            for row in results:
                print(row)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Ensure session is closed
        if 'connector' in locals():
            connector.close_session()

if __name__ == "__main__":
    main()
