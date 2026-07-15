"""Import Required dependencies"""
from .git import Git
from rich.console import Console


git = Git()
console = Console()


def build_prompt(diff_stat: str, raw_diff: str) -> str:
    """
    *Builds Prompts*

    Usage:
        build_prompt(diff_stat=git_diff_stat,raw_diff=git_diff)

    Args:
        diff_stat:
            str: The Git Diif Stat

        raw_diff:
            str: The raw git diff

    Return:
        str: prompt for LLM with an NOTE if raw_diff exceds over 4000 chars
    """
    note = ""
    if len(raw_diff) > 4000:
        console.print('[yellow]Diff truncated at 4000 chars.[/]')
        note = "\n\n**Note: The diff was truncated to the first 4000 characters.**"

    return f"""
    Generate ONE conventional commit message.

    Changed files:
    {diff_stat}
    {note}

    Diff:
    {raw_diff[:4000]}
    """

def push():
    git.is_repo()

    
