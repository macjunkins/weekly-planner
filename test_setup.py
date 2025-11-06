#!/usr/bin/env python3
"""
Test script to verify weekly-planner setup and dependencies.
This validates that the repo is working and can be run.
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required Python packages are installed."""
    required_packages = [
        'gql',
        'yaml',  # PyYAML
        'dotenv',  # python-dotenv
        'git',  # GitPython
        'dateutil',  # python-dateutil
        'rich',
        'icalendar',
        'pytz'
    ]

    missing = []
    installed = []

    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)

    return installed, missing

def check_configuration():
    """Check if configuration files exist and are valid."""
    config_file = Path('config.yaml')
    env_file = Path('.env')

    results = {}

    # Check config.yaml
    if config_file.exists():
        try:
            import yaml
            with open(config_file) as f:
                config = yaml.safe_load(f)
                results['config.yaml'] = {
                    'exists': True,
                    'valid': True,
                    'projects': len(config.get('projects', []))
                }
        except Exception as e:
            results['config.yaml'] = {
                'exists': True,
                'valid': False,
                'error': str(e)
            }
    else:
        results['config.yaml'] = {'exists': False}

    # Check .env
    results['.env'] = {'exists': env_file.exists()}

    return results

def check_lib_directory():
    """Check if lib directory symlink is working."""
    lib_dir = Path('lib')

    if not lib_dir.exists():
        return {'exists': False}

    if not lib_dir.is_symlink():
        return {'exists': True, 'is_symlink': False}

    target = lib_dir.resolve()
    files = list(lib_dir.glob('*.py'))

    return {
        'exists': True,
        'is_symlink': True,
        'target': str(target),
        'accessible': len(files) > 0,
        'files': [f.name for f in files]
    }

def main():
    """Run all checks and display results."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    console = Console()

    console.print("\n[bold cyan]Weekly Planner - Setup Verification[/bold cyan]\n")

    # Check dependencies
    console.print("[bold yellow]1. Checking Python Dependencies...[/bold yellow]")
    installed, missing = check_dependencies()

    if installed:
        console.print(f"[green]✓ Installed ({len(installed)}):[/green] {', '.join(installed)}")

    if missing:
        console.print(f"[red]✗ Missing ({len(missing)}):[/red] {', '.join(missing)}")
        console.print("[yellow]Run:[/yellow] pip install -r requirements.txt")
    else:
        console.print("[green]✓ All dependencies installed![/green]")

    # Check configuration
    console.print("\n[bold yellow]2. Checking Configuration Files...[/bold yellow]")
    config_results = check_configuration()

    for filename, result in config_results.items():
        if result['exists']:
            if filename == 'config.yaml':
                if result.get('valid'):
                    console.print(f"[green]✓ {filename}:[/green] Valid YAML with {result['projects']} projects")
                else:
                    console.print(f"[red]✗ {filename}:[/red] Invalid - {result.get('error')}")
            else:
                console.print(f"[green]✓ {filename}:[/green] Found")
        else:
            console.print(f"[yellow]⚠ {filename}:[/yellow] Not found")
            if filename == '.env':
                console.print("  [dim]Create from:[/dim] cp .env.example .env")

    # Check lib directory
    console.print("\n[bold yellow]3. Checking Shared Library...[/bold yellow]")
    lib_result = check_lib_directory()

    if lib_result['exists']:
        if lib_result.get('is_symlink'):
            if lib_result.get('accessible'):
                console.print(f"[green]✓ lib/:[/green] Symlink working")
                console.print(f"  [dim]Target:[/dim] {lib_result['target']}")
                console.print(f"  [dim]Files:[/dim] {', '.join(lib_result['files'])}")
            else:
                console.print("[yellow]⚠ lib/:[/yellow] Symlink exists but target not accessible")
        else:
            console.print("[yellow]⚠ lib/:[/yellow] Directory exists but not a symlink")
    else:
        console.print("[red]✗ lib/:[/red] Not found")
        console.print("  [dim]Create with:[/dim] ln -s ../portfolio-manager/lib lib")

    # Summary
    console.print("\n[bold yellow]4. Overall Status[/bold yellow]")

    can_run = not missing and config_results['config.yaml']['exists']
    has_env = config_results['.env']['exists']

    if can_run and has_env:
        console.print(Panel(
            "[bold green]✓ All checks passed![/bold green]\n\n"
            "The weekly-planner repository is properly configured and ready to use.\n"
            "You can now run scripts once they are implemented (currently in M1 development).",
            title="Status: Ready",
            border_style="green"
        ))
        return 0
    elif can_run and not has_env:
        console.print(Panel(
            "[bold yellow]⚠ Almost ready![/bold yellow]\n\n"
            "Dependencies are installed but you need to create a .env file:\n"
            "1. Copy .env.example to .env\n"
            "2. Add your GitHub token with repo, read:org, read:user scopes",
            title="Status: Configuration Needed",
            border_style="yellow"
        ))
        return 1
    else:
        console.print(Panel(
            "[bold red]✗ Setup incomplete[/bold red]\n\n"
            "Please resolve the issues above before running weekly-planner.",
            title="Status: Not Ready",
            border_style="red"
        ))
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
