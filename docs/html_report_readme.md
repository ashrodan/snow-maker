# HTML Change Report Generator

## Overview
This script generates an interactive HTML report for Snowflake configuration changes, featuring:
- Pie chart visualization of change status
- Detailed tables of database and warehouse modifications
- Responsive design with Chart.js integration

## Prerequisites
- Python 3.7+
- Web browser to view the report

## Usage
1. Generate the report:
```bash
python scripts/change_report_html_generator.py
```

2. Open the generated report in a web browser:
```bash
open change_report.html  # macOS
xdg-open change_report.html  # Linux
start change_report.html  # Windows
```

## Customization
- Modify input JSON file:
```bash
python scripts/change_report_html_generator.py --input custom_changes.json --output custom_report.html
```

## Features
- Automatically reads from `changes.json`
- Generates a standalone, interactive HTML report
- Embeds Chart.js for dynamic pie chart visualization
- Responsive design for various screen sizes
