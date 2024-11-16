# Change Report Visualization Options

## 1. Terminal/Console Visualization

```
❄️ Snow-Maker Change Report 📊
===============================
Total Objects: 3
✅ Objects Created:   2
🔄 Objects Updated:   1
❌ Objects with Errors: 0

📦 Database Changes:
--------------------
[CREATED] ANALYTICS Database
[CREATED] STAGING Database

🏭 Warehouse Changes:
---------------------
[UPDATED] COMPUTE_WH Warehouse
  Changes:
  - size: X-SMALL → MEDIUM
  - auto_suspend: 600 → 300
  - auto_resume: TRUE → true
  - comment: (empty) → "GENERAL COMPUTE WAREHOUSE"
```

## 2. HTML Interactive Dashboard

```html
<!DOCTYPE html>
<html>
<head>
    <title>Snow-Maker Change Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; }
        .summary { display: flex; justify-content: space-around; }
        .changes { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Snow-Maker Change Report</h1>
    
    <div class="summary">
        <div>
            <h2>Object Status</h2>
            <canvas id="statusChart"></canvas>
        </div>
        <div>
            <h2>Summary Statistics</h2>
            <ul>
                <li>Total Objects: 3</li>
                <li>Objects Created: 2</li>
                <li>Objects Updated: 1</li>
                <li>Objects with Errors: 0</li>
            </ul>
        </div>
    </div>

    <div class="changes">
        <h2>Detailed Changes</h2>
        <div id="databaseChanges">
            <h3>Database Changes</h3>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td>ANALYTICS</td>
                    <td>Database</td>
                    <td>CREATED</td>
                </tr>
                <tr>
                    <td>STAGING</td>
                    <td>Database</td>
                    <td>CREATED</td>
                </tr>
            </table>
        </div>
        <div id="warehouseChanges">
            <h3>Warehouse Changes</h3>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Field</th>
                    <th>Old Value</th>
                    <th>New Value</th>
                </tr>
                <tr>
                    <td rowspan="4">COMPUTE_WH</td>
                    <td>size</td>
                    <td>X-SMALL</td>
                    <td>MEDIUM</td>
                </tr>
                <tr>
                    <td>auto_suspend</td>
                    <td>600</td>
                    <td>300</td>
                </tr>
                <tr>
                    <td>auto_resume</td>
                    <td>TRUE</td>
                    <td>true</td>
                </tr>
                <tr>
                    <td>comment</td>
                    <td>(empty)</td>
                    <td>GENERAL COMPUTE WAREHOUSE</td>
                </tr>
            </table>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('statusChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Created', 'Updated', 'No Change', 'Errors'],
                datasets: [{
                    data: [2, 1, 0, 0],
                    backgroundColor: ['green', 'orange', 'gray', 'red']
                }]
            }
        });
    </script>
</body>
</html>
```

## 3. Python Rich CLI Visualization

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def visualize_changes(changes_data):
    console = Console()

    # Summary Panel
    summary_panel = Panel(
        f"Total Objects: {changes_data['total_objects']}\n"
        f"Objects Created: {changes_data['objects_created']}\n"
        f"Objects Updated: {changes_data['objects_updated']}\n"
        f"Objects with Errors: {changes_data['objects_with_errors']}",
        title="Change Report Summary",
        border_style="bold blue"
    )
    console.print(summary_panel)

    # Database Changes Table
    db_table = Table(title="Database Changes")
    db_table.add_column("Name", style="cyan")
    db_table.add_column("Type", style="magenta")
    db_table.add_column("Status", style="green")

    for db in changes_data['changes']['database']:
        db_table.add_row(db['name'], db['type'], db['status'])
    
    console.print(db_table)

    # Warehouse Changes Table
    wh_table = Table(title="Warehouse Changes")
    wh_table.add_column("Name", style="cyan")
    wh_table.add_column("Field", style="magenta")
    wh_table.add_column("Old Value", style="red")
    wh_table.add_column("New Value", style="green")

    for wh in changes_data['changes']['warehouse']:
        for diff in wh['differences']:
            wh_table.add_row(
                wh['name'], 
                diff['field'], 
                str(diff['actual']), 
                str(diff['expected'])
            )
    
    console.print(wh_table)
