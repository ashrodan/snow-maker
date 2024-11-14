# Contributing to Snowflake Connector Project

## Welcome Contributors!

We appreciate your interest in contributing to the Snowflake Connector Project. This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your forked repository
3. Create a new branch for your feature or bugfix

## Development Setup

### Prerequisites
- Python 3.7+
- pip
- virtualenv (recommended)

### Setup Steps
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r tests/requirements.txt
```

## Development Workflow

### Running Tests
```bash
pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Maintain consistent code formatting

## Contribution Process

1. Create an issue describing the feature/bugfix
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Write/update tests
6. Ensure all tests pass
7. Submit a pull request

### Pull Request Guidelines
- Provide a clear, descriptive title
- Include a summary of changes
- Reference related issues
- Ensure all tests pass
- Include any necessary documentation updates

## Reporting Issues
- Use GitHub Issues
- Provide a clear description
- Include steps to reproduce
- Share error messages and stack traces
- Specify your environment (Python version, OS, etc.)

## Code of Conduct
- Be respectful and inclusive
- Collaborate constructively
- Help create a positive community

## Questions?
If you have questions, please open an issue or reach out to the maintainers.

Thank you for contributing!
