# Snowflake Connector Project

## Project Structure
```
snowflake_project/
│
├── main.py                     # Main entry point
├── requirements.txt            # Project dependencies
│
├── src/
│   └── snowflake_connector/
│       ├── connection.py       # Snowflake connection management
│       └── utils/
│           └── config_loader.py # Configuration loading utility
│
└── tests/                      # Future test directory
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Credentials
- Create `.env.dev`, `.env.tst`, or `.env.prd` files
- Add Snowflake connection parameters:
  ```
  SNOWFLAKE_ACCOUNT=your_account
  SNOWFLAKE_USER=your_username
  SNOWFLAKE_PASSWORD=your_password
  SNOWFLAKE_DATABASE=your_database
  SNOWFLAKE_SCHEMA=your_schema
  SNOWFLAKE_ROLE=your_role
  SNOWFLAKE_WAREHOUSE=your_warehouse
  ```

## Usage

### List Databases
```bash
python main.py -l
```

### Connect to Specific Environment
```bash
python main.py -e tst  # Connect to test environment
```

### Execute Custom Query
```bash
python main.py -q "SELECT CURRENT_VERSION()"
```

## Features
- Environment-specific configuration
- Flexible connection management
- Simple CLI interface
- Modular project structure

## Configuration Options
- `-e, --env`: Specify environment (dev/tst/prd)
- `-l, --list-databases`: List available databases
- `-q, --query`: Execute a custom SQL query

## Error Handling
- Validates required Snowflake connection parameters
- Provides informative error messages
- Ensures proper session management

## Future Improvements
- Add comprehensive logging
- Implement more advanced query handling
- Create unit and integration tests
