import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def visualize_changes(changes_file='changes.json'):
    """
    Visualize changes from a JSON change report using Rich library.
    
    :param changes_file: Path to the changes JSON file
    """
    # Read changes from JSON file
    with open(changes_file, 'r') as f:
        changes_data = json.load(f)

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

def main():
    visualize_changes()

if __name__ == "__main__":
    main()
