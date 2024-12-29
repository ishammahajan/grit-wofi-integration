import subprocess
import re

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
        return {
            "id": task_id,
            "name": name,
            "status": status,
            "display": f"{status} {name}"
        }
    return None

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
