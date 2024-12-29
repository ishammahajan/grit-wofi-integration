import subprocess
import re
import json
import os

def get_state_file_path():
    """Get the path to the state file in /tmp"""
    return '/tmp/grit-wofi-state.json'

def save_navigation_state(task_stack):
    """Save the current navigation state to tmp file"""
    try:
        with open(get_state_file_path(), 'w') as f:
            json.dump([task for task in task_stack], f)
    except Exception as e:
        print(f"Error saving state: {e}")

def load_navigation_state():
    """Load the navigation state from tmp file"""
    try:
        if os.path.exists(get_state_file_path()):
            with open(get_state_file_path(), 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading state: {e}")
    return []

def parse_task_line(line):
    """
    Parse a task line to extract ID and name
    Example: "[ ] feudships (1)" -> {"id": "1", "name": "feudships", "status": "[ ]"}
    """
    # Match pattern: status, name, and ID in parentheses
    pattern = r'(\[[ x]\]) (.*?) \((\d+)\)'
    match = re.match(pattern, line.strip())
    
    if match:
        status, name, task_id = match.groups()
        # Create display string - add checkmark if task is done
        display = f"{name} (✔)" if status == "[x]" else name
        return {
            "id": task_id,
            "name": name,
            "status": status,
            "display": display
        }
    return None

def add_subtask(parent_id, task_name):
    """Add a new subtask"""
    try:
        cmd = ['grit', 'add']
        if parent_id:
            cmd.extend(['-p', parent_id])
        else:
            cmd.append('-r')
        cmd.append(task_name)
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_task(task_id):
    """Mark a task as done"""
    try:
        subprocess.run(['grit', 'check', task_id], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def remove_task(task_id):
    """Remove a task"""
    try:
        subprocess.run(['grit', 'rm', task_id], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_tasks_at_level(task_id=None):
    """
    Get tasks at a specific level
    
    Args:
        task_id (str, optional): The parent task ID. If None, gets root tasks
    
    Returns:
        list: List of task dictionaries with id, name, and status
    """
    try:
        cmd = ['grit', 'ls']
        if task_id:
            cmd.append(task_id)
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip()
        
        tasks = []
        for line in output.split('\n'):
            if line.strip():
                task = parse_task_line(line)
                if task:
                    tasks.append(task)
        
        return tasks
        
    except subprocess.CalledProcessError:
        return []
    except FileNotFoundError:
        return []
