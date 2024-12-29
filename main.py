#!/usr/bin/env python3
import subprocess
from grit_functions import get_tasks_at_level, add_subtask, check_task, remove_task

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

def get_action_items(current_task=None):
    """Get the list of possible actions"""
    if current_task:
        # Actions for a specific task
        return [
            {"id": "add", "display": "➕ Add subtask to: " + current_task["name"]},
            {"id": "check", "display": "✓ Mark as done: " + current_task["name"]},
            {"id": "remove", "display": "❌ Remove: " + current_task["name"]},
            {"id": "up", "display": "⬅️ Go back"}
        ]
    else:
        # Root level actions
        return [
            {"id": "add_root", "display": "➕ Add new root task"},
            {"id": "up", "display": "⬅️ Exit"}
        ]

def navigate_tasks():
    """Interactive task navigation"""
    current_task_id = None
    task_stack = load_navigation_state()
    current_task_id = task_stack[-1]["id"] if task_stack else None
    
    while True:
        # Get tasks at current level
        tasks = get_tasks_at_level(current_task_id)
        current_task = task_stack[-1] if task_stack else None
        
        # Combine tasks and actions into one list
        all_items = []
        if tasks:
            all_items.extend(tasks)
        all_items.extend(get_action_items(current_task))
        
        # Create prompt showing current path
        prompt = " > ".join([t["name"] for t in task_stack]) or "Root"
        
        # Show combined list in wofi
        selected = show_wofi_dialog(all_items, prompt=prompt)
        
        if not selected:
            break
            
        # Handle selection based on whether it's a task or action
        if "id" in selected and selected["id"] in ["add", "check", "remove", "up", "add_root"]:
            # Handle actions
            if selected["id"] == "add" or selected["id"] == "add_root":
                try:
                    wofi_cmd = ['wofi', '--show', 'dmenu', '--prompt', 'Enter task name']
                    process = subprocess.Popen(wofi_cmd,
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            text=True)
                    task_name, _ = process.communicate(input='\n')
                    task_name = task_name.strip()
                    
                    if task_name:
                        if selected["id"] == "add_root":
                            add_subtask(None, task_name)  # Add root task
                        else:
                            add_subtask(current_task["id"], task_name)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
                    
            elif selected["id"] == "check":
                if check_task(current_task["id"]):
                    if task_stack:
                        task_stack.pop()
                        current_task_id = task_stack[-1]["id"] if task_stack else None
                    
            elif selected["id"] == "remove":
                if remove_task(current_task["id"]):
                    if task_stack:
                        task_stack.pop()
                        current_task_id = task_stack[-1]["id"] if task_stack else None
                    
            elif selected["id"] == "up":
                if task_stack:
                    task_stack.pop()
                    current_task_id = task_stack[-1]["id"] if task_stack else None
                else:
                    break
                    
        # Save state after each navigation action
        save_navigation_state(task_stack)
                    
        else:
            # User selected a task - drill down
            task_stack.append(selected)
            current_task_id = selected["id"]

def main():
    navigate_tasks()

if __name__ == "__main__":
    main()
