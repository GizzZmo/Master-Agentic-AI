"""
Code Interpreter Tool - Simulated code execution functionality.
In a production environment, this would run in a secure sandboxed environment.
"""
from typing import Dict, Any
import re

def code_interpreter(code: str, language: str = "python") -> str:
    """
    Simulate code interpretation and execution.
    In production, this would execute code in a secure sandbox environment.
    """
    language = language.lower()
    code = code.strip()
    
    # Simulate different language outputs
    if language in ["python", "py"]:
        return _simulate_python_execution(code)
    elif language in ["javascript", "js", "node"]:
        return _simulate_javascript_execution(code)
    elif language in ["bash", "shell", "sh"]:
        return _simulate_shell_execution(code)
    elif language in ["sql"]:
        return _simulate_sql_execution(code)
    else:
        return f"Code interpretation for {language}:\n{code}\n\nOutput: [Simulated execution - language '{language}' processed successfully]"

def _simulate_python_execution(code: str) -> str:
    """Simulate Python code execution."""
    # Simple pattern matching for common Python operations
    if "print(" in code:
        # Extract print statements
        print_matches = re.findall(r'print\((.*?)\)', code)
        output = "Python execution output:\n"
        for match in print_matches:
            # Simple evaluation simulation
            if match.strip().startswith('"') or match.strip().startswith("'"):
                # String literal
                output += match.strip().strip('"\'') + "\n"
            elif match.strip().isdigit():
                # Number
                output += match.strip() + "\n"
            else:
                # Variable or expression
                output += f"[Result of {match.strip()}]\n"
        return output
    
    elif "def " in code:
        func_name = re.search(r'def\s+(\w+)', code)
        name = func_name.group(1) if func_name else "function"
        return f"Python execution output:\nFunction '{name}' defined successfully."
    
    elif "import " in code or "from " in code:
        return "Python execution output:\nModules imported successfully."
    
    elif any(op in code for op in ["+", "-", "*", "/", "**"]):
        return "Python execution output:\nMathematical operation completed successfully."
    
    else:
        return f"Python execution output:\nCode executed successfully:\n{code}"

def _simulate_javascript_execution(code: str) -> str:
    """Simulate JavaScript code execution."""
    if "console.log(" in code:
        log_matches = re.findall(r'console\.log\((.*?)\)', code)
        output = "JavaScript execution output:\n"
        for match in log_matches:
            if match.strip().startswith('"') or match.strip().startswith("'"):
                output += match.strip().strip('"\'') + "\n"
            else:
                output += f"[Result of {match.strip()}]\n"
        return output
    
    elif "function " in code:
        func_name = re.search(r'function\s+(\w+)', code)
        name = func_name.group(1) if func_name else "function"
        return f"JavaScript execution output:\nFunction '{name}' defined successfully."
    
    else:
        return f"JavaScript execution output:\nCode executed successfully:\n{code}"

def _simulate_shell_execution(code: str) -> str:
    """Simulate shell command execution."""
    commands = code.split('\n')
    output = "Shell execution output:\n"
    
    for cmd in commands:
        cmd = cmd.strip()
        if not cmd:
            continue
            
        if cmd.startswith('ls'):
            output += "file1.txt  file2.py  directory/\n"
        elif cmd.startswith('pwd'):
            output += "/current/working/directory\n"
        elif cmd.startswith('echo'):
            text = cmd.replace('echo ', '', 1)
            output += text + "\n"
        elif cmd.startswith('mkdir'):
            dir_name = cmd.replace('mkdir ', '', 1)
            output += f"Directory '{dir_name}' created.\n"
        else:
            output += f"Command '{cmd}' executed successfully.\n"
    
    return output

def _simulate_sql_execution(code: str) -> str:
    """Simulate SQL query execution."""
    code_upper = code.upper()
    
    if "SELECT" in code_upper:
        return "SQL execution output:\nQuery executed successfully. Sample results:\nRow 1: [data]\nRow 2: [data]\n3 rows returned."
    elif "INSERT" in code_upper:
        return "SQL execution output:\nINSERT statement executed successfully. 1 row affected."
    elif "UPDATE" in code_upper:
        return "SQL execution output:\nUPDATE statement executed successfully. Rows affected: 2."
    elif "DELETE" in code_upper:
        return "SQL execution output:\nDELETE statement executed successfully. Rows affected: 1."
    elif "CREATE" in code_upper:
        return "SQL execution output:\nTable/structure created successfully."
    else:
        return f"SQL execution output:\nQuery executed successfully:\n{code}"

# Alternative function names
execute_code = code_interpreter
run_code = code_interpreter