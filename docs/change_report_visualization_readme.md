# Change Report Visualization Script

## Overview
This script provides a rich, colorful terminal-based visualization of Snowflake configuration changes using the Rich library.

## Prerequisites
- Python 3.7+
- pip

## Setup
1. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Usage
Run the script directly:
```bash
python scripts/change_report_visualizer.py
```

Or import and use in another script:
```python
from change_report_visualizer import visualize_changes

# Visualize changes from a specific JSON file
visualize_changes('path/to/changes.json')
```

## Example Output
The script will generate a terminal output with:
- A summary panel showing total objects and change statistics
- A table of database changes
- A table of warehouse changes with detailed modifications
