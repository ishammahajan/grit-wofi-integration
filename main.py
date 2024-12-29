#!/usr/bin/env python3
import subprocess
import json

def get_grit_tasks():
    """Get current tasks from grit"""
    try:
        # Run 'grit' command and capture output
        result = subprocess.run(['grit'], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Error: Could not fetch grit tasks"
    except FileNotFoundError:
        return "Error: grit command not found"

def show_wofi_dialog(tasks):
    """Display tasks in wofi"""
    try:
        # Pipe tasks to wofi
        wofi_cmd = ['wofi', '--show', 'dmenu', '--prompt', 'Grit Tasks']
        process = subprocess.Popen(wofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output, _ = process.communicate(input=tasks)
        return output
    except subprocess.CalledProcessError:
        print("Error: Could not display wofi dialog")
    except FileNotFoundError:
        print("Error: wofi command not found")

def main():
    # Get tasks from grit
    tasks = get_grit_tasks()
    
    # Show tasks in wofi
    if tasks:
        show_wofi_dialog(tasks)

if __name__ == "__main__":
    main()
