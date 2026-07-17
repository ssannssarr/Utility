"""Import Required dependencies"""
import sys
from rich.console import Console
from .git import Git,GitError
from .api import OpenAI
from .helpers import (
    build_prompt,
    commit_msg,
    confirmation,
    get_remote_branch,
    status,
    Workflow
)

ai = OpenAI()
git = Git()
console = Console()

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
            commit = git.commit(msg=msg).stderr

        if config.remote_branch_confirm:
            remote, branch = get_remote_branch()
        else:
            remote = None
            branch = None

        with status("Pushing The Changes to remote..."):
            pushout = git.push(remote=remote,branch=branch).stderr


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
