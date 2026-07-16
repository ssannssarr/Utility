"""Import Required dependencies"""
from contextlib import contextmanager
from dataclasses import dataclass
from rich.console import Console


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

def confirmation(que: str) -> bool:
    """
    *It Prompts A comfirmation input*

    Args:
        que:
            str: The question
    Usage:
        confirmation('Enter your choice!')

    Returns:
        bool: True if y or yes and Fasle if n or no
    """
    while True:
        console.print(f'[yellow]{que}[/]')
        confirm = input(': ').lower().strip()
        if confirm not in {'y','n','yes','no'}:
            continue

        if confirm not in {'y','yes'}:
            return False

        return True

@contextmanager
def status(msg: str):
    """
    *For const theme status renderer*
    Args:
        msg:
            str: The status messasge that has to be rendered

    Usage:
        with status("Getting diff.."):
            #your code block here
            pass

    Yeilds:
        rich.status: {arc} Your message!
    """
    with console.status(
        f"[#ffebcd]{msg}[/]",
        spinner="arc",
        spinner_style="#00ffff"
    ):
        yield

def commit_msg() -> str:
    """
    *Takes custom commit msg if User didnt liked the msg given by llm*

    Args:
        None

    Usage:
        msg = commit_msg()

    Returns:
        str: The commit msg written by the User
    """
    console.print("[yellow]Enter Commit msg;")
    while True:
        msg = input(': ')
        if not msg:
            continue

        return msg

def get_remote_branch():
    """
    *Get remote and Branch name*

    Args:
        None

    Usage:
        remote, branch = get_remote_barnch()

    Returns:
        tuple: (remote,branch)
    """

    console.print("[yellow]Enter remote name..[/]")
    while True:
        remote = input(": ")
        if not remote:
            continue
        break

    console.print("[yellow]Enter Branch name...[/]")
    while True:
        branch = input(": ")
        if not branch:
            continue
        break

    return remote, branch

@dataclass(frozen=True)
class Workflow:
    """Confirmation Config Class for push workflow"""
    branch_confirm: bool
    ask_files: bool
    commit_confirm: bool
    remote_branch_confirm: bool
