# Snow-Maker

Snow-Maker is a Python wrapper for Snowflake, designed to streamline the configuration and provisioning of Snowflake components programmatically. It abstracts complex operations into simple configurations, enabling efficient management of Snowflake resources, automation of workflows, and seamless integration with existing data pipelines.

```
python snowflake_connection.py --env dev --output changes.json
```

## Features

- **Configuration as Code**: Define Snowflake resources using configuration files.
- **Automation Tools**: CLI tools for schema creation, data loading, and query execution.
- **Integration Support**: Integrate with popular data processing frameworks.
- **Testing Framework**: Validate configurations and changes before deployment.
- **Extensibility**: Plugin system for custom extensions and integrations.
- **Security**: Role-based access control and data encryption.
- **Change Reporting**: Comprehensive tracking and reporting of configuration changes

## Change Reporting Feature

### Overview

The Change Reporting feature provides a robust mechanism for tracking, analyzing, and reporting configuration changes in Snowflake resources. This advanced functionality allows users to:

- Perform dry runs to preview potential configuration modifications
- Generate detailed, structured reports of configuration changes
- Export change reports in JSON format for further analysis
- Track object creation, updates, deletions, and errors

### Key Components

1. **ChangeStatus Enum**
   - Tracks the state of each object: `NO_CHANGE`, `CREATED`, `UPDATED`, `DELETED`, `ERROR`
   - Provides a clear, standardized way to represent configuration change states

2. **ObjectChangeEntry**
   - Captures detailed information about individual object changes
   - Includes object name, type, status, and specific differences
   - Supports error tracking for failed configuration operations

3. **ChangeReport**
   - Aggregates changes across multiple object types
   - Provides summary statistics:
     * Total objects processed
     * Objects created
     * Objects updated
     * Objects with no changes
     * Objects with errors

### Usage Example

```bash
# Perform a dry run and export change report
python snowflake_connection.py --dry-run --output changes.json
```

### Benefits

- **Transparency**: Clear visibility into configuration changes
- **Risk Mitigation**: Preview changes before applying them
- **Compliance**: Detailed audit trail of configuration modifications
- **Flexibility**: Supports various reporting and integration scenarios

## Getting Started

### Prerequisites

- Python 3.x
- Snowflake Python SDK
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd snow-maker
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Define your Snowflake resources in the `config/` directory.
2. Use the CLI tools in the `scripts/` directory to manage your Snowflake environment.

### Testing

Run tests using the following command:
```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
