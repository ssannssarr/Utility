"""Import Required dependencies"""
from contextlib import contextmanager
import sys
from dataclasses import dataclass
from rich.console import Console
from .git import Git,GitError
from .api import OpenAI

ai = OpenAI()
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

NORMAL = Workflow(
    branch_confirm=True,
    ask_files=True,
    commit_confirm=True,
    remote_branch_confirm=True
)

YOLO = Workflow(
    branch_confirm=False,
    ask_files=False,
    commit_confirm=True,
    remote_branch_confirm=False
)

def push(config: Workflow):
    """
    *This the main code block that does add, commit and push*

    Args:
        config: Worflow

    Usage:
        Well you can use this so many ways but I am gonna use it in cli using click module
    """
    if not git.is_repo():
        raise GitError("Not inside Repo!")

    try:
        console.print(f"[#ffebcd]Pushing on brach[/] [cyan]{git.branch().stdout}[/]")
        if config.branch_confirm:
            branch_conf = confirmation("Do you want to push into this branch ?? y/n")

            if not branch_conf:
                console.print("[#ffebcd]Switch To Your Preffered Branch;[/]")
                sys.exit()

        if config.ask_files:
            files = input("Files or  Options to git add cmd: ")
        else:
            files = "-A"
        with status("Adding Files..."):
            add_out = git.add(files=files).stdout
        console.print(add_out)

        with status(msg="Getting Diff..."):
            diff_stat = git.diff("--staged --stat").stdout
            raw_diff = git.diff("--staged -z").stdout
            if not raw_diff:
                console.print("[yellow]No Changes No Commit.[/]")
                sys.exit()

        with status("Getting Commit msg from llm..."):
            prompt = build_prompt(diff_stat=diff_stat,raw_diff=raw_diff)
            msg, model = ai.ask(prompt=prompt)

        console.print(f'{model}: {msg}')
        if config.commit_confirm:
            commit_conf = confirmation(que="Will You use this msg? y/n ")
            if not commit_conf:
                msg = commit_msg()

        with status("Commiting The Changes..."):
            commit = git.commit(msg=msg)

        if config.remote_branch_confirm:
            remote, branch = get_remote_branch()
        else:
            remote = None
            branch = None

        with status("Pushing The Changes to remote..."):
            push = git.push(remote=remote,branch=branch)


        console.print("[#00ffff]DONE![/]")
    except GitError as e:
        console.print(f"{type(e).__name__}:{str(e)}")
        console.print(git.reset().stdout)
    except KeyboardInterrupt:
        console.print("[yellow]Aborted By user..[/]")
        console.print(git.reset().stdout)
    except Exception as e:
        console.print(git.reset().stdout)
        console.print(e)


if __name__ == "__main__":
    push(YOLO)
