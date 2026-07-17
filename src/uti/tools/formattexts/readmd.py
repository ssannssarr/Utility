"""Import Required Dependences"""
import sys
from rich.console import Console
from rich.markdown import Markdown as mdout

console = Console()

def main():
    """
    **The Main Code Block**
    [This prints out Markdown formated text]

    Args:
        None

    Usage:
        $ cat <file-name> | uti format md

    Returns:
        MarkDown: Prints Out Markdown Formated text

    /* WHY: Becasue glow takes more startup time than python.rich in my machine */
    """
    mdtext = sys.stdin.read()
    console.print(mdout(mdtext))

if __name__ == "__main__":
    main()
