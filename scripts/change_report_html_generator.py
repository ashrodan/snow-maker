import json
import os

def generate_html_report(changes_file='changes.json', output_file='change_report.html'):
    """
    Generate an HTML report from a changes JSON file.
    
    :param changes_file: Path to the changes JSON file
    :param output_file: Path to save the generated HTML report
    """
    # Read changes from JSON file
    with open(changes_file, 'r') as f:
        changes_data = json.load(f)

    # HTML Template with embedded Chart.js for visualization
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Snow-Maker Change Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .summary {{ display: flex; justify-content: space-around; margin-bottom: 30px; }}
            .changes {{ margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
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
                    <li>Total Objects: {changes_data['total_objects']}</li>
                    <li>Objects Created: {changes_data['objects_created']}</li>
                    <li>Objects Updated: {changes_data['objects_updated']}</li>
                    <li>Objects with Errors: {changes_data['objects_with_errors']}</li>
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
                    {"".join([f'<tr><td>{db["name"]}</td><td>{db["type"]}</td><td>{db["status"]}</td></tr>' for db in changes_data['changes']['database']])}
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
                    {"".join([f'<tr><td rowspan="{len(wh["differences"])}">{wh["name"]}</td><td>{diff["field"]}</td><td>{diff["actual"]}</td><td>{diff["expected"]}</td></tr>' for wh in changes_data['changes']['warehouse'] for diff in wh['differences']])}
                </table>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('statusChart').getContext('2d');
            new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: ['Created', 'Updated', 'No Change', 'Errors'],
                    datasets: [{{
                        data: [{changes_data['objects_created']}, {changes_data['objects_updated']}, 0, {changes_data['objects_with_errors']}],
                        backgroundColor: ['green', 'orange', 'gray', 'red']
                    }}]
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Write HTML to file
    with open(output_file, 'w') as f:
        f.write(html_template)
    
    print(f"HTML report generated: {os.path.abspath(output_file)}")

def main():
    generate_html_report()

if __name__ == "__main__":
    main()
