#!/usr/bin/env python3
"""
Test script to demonstrate that weekly-planner can use shared libraries.
This validates that the symlinked lib directory works correctly.
"""

import sys
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add lib to path so we can import from it
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from project_utils import load_config, get_priority_emoji

def main():
    """Demonstrate loading and displaying project configuration."""
    console = Console()

    console.print("\n[bold cyan]Weekly Planner - Library Integration Test[/bold cyan]\n")

    # Test 1: Load configuration using shared utility
    console.print("[bold yellow]1. Loading project configuration...[/bold yellow]")

    try:
        config_path = Path('config.yaml')
        config = load_config(str(config_path))
        console.print(f"[green]✓ Configuration loaded successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to load config:[/red] {e}")
        return 1

    # Test 2: Display project information
    console.print("\n[bold yellow]2. Project Portfolio Overview[/bold yellow]\n")

    projects = config.get('projects', [])

    if not projects:
        console.print("[red]No projects found in config![/red]")
        return 1

    # Group projects by pillar
    pillars = {}
    for project in projects:
        pillar = project.get('pillar', 'unknown')
        if pillar not in pillars:
            pillars[pillar] = []
        pillars[pillar].append(project)

    # Display summary by pillar
    for pillar, pillar_projects in pillars.items():
        table = Table(title=f"Pillar: {pillar.upper()}", show_header=True)
        table.add_column("Project", style="cyan")
        table.add_column("Priority", style="yellow")
        table.add_column("Description", style="dim")

        for proj in pillar_projects:
            name = proj.get('name', 'Unknown')
            priority = proj.get('priority', 'medium')
            description = proj.get('description', 'No description')

            # Use shared utility to format priority
            priority_display = f"{get_priority_emoji(priority)} {priority}"

            table.add_row(name, priority_display, description)

        console.print(table)
        console.print()

    # Test 3: Show configuration statistics
    console.print("[bold yellow]3. Configuration Statistics[/bold yellow]\n")

    stats = {
        'Total Projects': len(projects),
        'GitHub User': config.get('github', {}).get('user', 'Not set'),
        'Organizations': len(config.get('github', {}).get('organizations', [])),
        'Pillars': len(pillars),
        'Critical Priority': sum(1 for p in projects if p.get('priority') == 'critical'),
        'High Priority': sum(1 for p in projects if p.get('priority') == 'high'),
    }

    for key, value in stats.items():
        console.print(f"  [cyan]{key}:[/cyan] {value}")

    # Success summary
    console.print()
    console.print(Panel(
        "[bold green]✓ Library integration working![/bold green]\n\n"
        "The weekly-planner can successfully:\n"
        "• Import shared utilities from portfolio-manager\n"
        "• Load and parse YAML configuration\n"
        "• Access project data for planning\n\n"
        "Ready for M1 development work.",
        title="Status: Verified",
        border_style="green"
    ))

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        console.print("\n[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)