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
        errors='replace'
    )


