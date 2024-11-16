import json
import os
from datetime import datetime

def generate_markdown_report(changes_file='changes.json', output_file='change_report.md'):
    """
    Generate a GitHub-flavored Markdown report from a changes JSON file.
    
    :param changes_file: Path to the changes JSON file
    :param output_file: Path to save the generated Markdown report
    """
    # Read changes from JSON file
    with open(changes_file, 'r') as f:
        changes_data = json.load(f)

    # Prepare markdown content
    markdown_content = f"""# 🔄 Snowflake Configuration Change Report

## 📊 Summary Statistics
| Metric | Count |
|--------|-------|
| Total Objects | {changes_data['total_objects']} |
| Objects Created | {changes_data['objects_created']} |
| Objects Updated | {changes_data['objects_updated']} |
| Objects with No Changes | {changes_data.get('objects_no_change', 0)} |
| Objects with Errors | {changes_data.get('objects_with_errors', 0)} |

## 📝 Detailed Changes

### 💾 Database Changes
| Name | Type | Status |
|------|------|--------|
{os.linesep.join([f"| {db['name']} | {db['type']} | {db['status']} |" for db in changes_data['changes']['database']])}

### 🏭 Warehouse Changes
| Name | Field | Old Value | New Value |
|------|-------|-----------|-----------|
{os.linesep.join([f"| {wh['name']} | {diff['field']} | {diff['actual']} | {diff['expected']} |" for wh in changes_data['changes']['warehouse'] for diff in wh['differences']])}

## 🕒 Report Generated
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📋 Workflow Context
- **Workflow Run:** ${{github.workflow}}
- **Repository:** ${{github.repository}}
- **Ref:** ${{github.ref}}
- **Commit SHA:** ${{github.sha}}
"""

    # Write Markdown to file
    with open(output_file, 'w') as f:
        f.write(markdown_content)
    
    print(f"Markdown report generated: {os.path.abspath(output_file)}")

def main():
    generate_markdown_report()

if __name__ == "__main__":
    main()
