import subprocess

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
