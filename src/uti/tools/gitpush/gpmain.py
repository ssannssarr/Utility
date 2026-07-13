"""Import Required dependencies"""
import subprocess as sp 
import sys
from rich.console import Console

console = Console()

def run(cmd: str) -> str:
    """Runs an Cmd and returns"""
    return sp.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replce'
    )
    
def is_repo():
    """It Checks the folder for either its git repo or not."""
    if run("git rev-parse --is-inside-work-tree").returncode != 0:
        console.print("[red]Not Inside Git Repo")
        sys.exit()
        
def is_branch():
    """This checks for either on branch or not"""
    branch = run(["git",'branch','--show-current']).stdout.strip() or ''
		if not branch:
			c.print('[red]Detached HEAD detected. Please checkout a branch before using gitpush-y.[/]')
			exit()