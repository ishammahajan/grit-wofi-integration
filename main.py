#!/usr/bin/env python3
import subprocess
from grit_functions import get_tasks_at_level

def show_wofi_dialog(tasks, prompt="Grit Tasks"):
    """
    Display tasks in wofi
    
    Args:
        tasks (list): List of task dictionaries
        prompt (str): Prompt to display in wofi
    
    Returns:
        dict: Selected task dictionary or None
    """
    try:
        # Create display strings for wofi
        display_items = [task["display"] for task in tasks]
        
        # Pipe tasks to wofi
        wofi_cmd = ['wofi', '--show', 'dmenu', '--prompt', prompt]
        process = subprocess.Popen(wofi_cmd, 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 text=True)
        
        output, _ = process.communicate(input='\n'.join(display_items))
        selected = output.strip()
        
        # Find the selected task
        for task in tasks:
            if task["display"] == selected:
                return task
                
        return None
        
    except subprocess.CalledProcessError:
        print("Error: Could not display wofi dialog")
    except FileNotFoundError:
        print("Error: wofi command not found")

def navigate_tasks():
    """Interactive task navigation"""
    current_task_id = None
    task_stack = []
    
    while True:
        # Get tasks at current level
        tasks = get_tasks_at_level(current_task_id)
        
        if not tasks:
            print("No tasks found at this level")
            break
            
        # Create prompt showing current path
        prompt = " > ".join([t["name"] for t in task_stack]) or "Root"
        
        # Show tasks in wofi
        selected = show_wofi_dialog(tasks, prompt=prompt)
        
        if not selected:
            # User cancelled - go up one level
            if task_stack:
                task_stack.pop()
                current_task_id = task_stack[-1]["id"] if task_stack else None
            else:
                break
        else:
            # User selected a task - drill down
            task_stack.append(selected)
            current_task_id = selected["id"]

def main():
    navigate_tasks()

if __name__ == "__main__":
    main()
