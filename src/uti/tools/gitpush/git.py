"""Import Required Dependencies"""
import subprocess as sp
from subprocess import CompletedProcess,CalledProcessError
from functools import wraps

def execute(cmd: str) -> CompletedProcess :
    """execute's an Cmd and returns"""
    return sp.run(
        cmd,
        check=True,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

class GitError(Exception):
    """The GitError Class"""
    def __init__(self, message: str):
        """Custom Message"""
        super().__init__(message)

def git_error(msg: str | None = None):
    """"""
    def decorator(func):
        """"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """"""
            try:
                return func(*args, **kwargs)
            except CalledProcessError as e:
                raise GitError(f"{msg}\n{e.stderr}") from e
        return wrapper
    return decorator


class Git:
    """Git helper Class"""
    @git_error("Failed to add files")
    def add(self,files: str) -> CompletedProcess :
        """
        *Adds passed files*

        Args:
            files: (you can use options also though XD)
                File names that you will add

        Usage:
            Git.add("-A")

        Returns:
            object: Complete Process
        """
        return execute(f"git add {files}")

    @git_error("Failed to commit")
    def commit(self,msg: str) -> CompletedProcess :
        """
        *Commits staged files*

        Args:
            msg:
                str: The Message for commit (or in simple 'commit message')

        Usage:
            Git.commit("Initail Commit")

        Returns:
            object: Complete process
        """
        return  execute(f'git commit -m "{msg}"')

    @git_error("Failed to execute diff")
    def diff(self,options: str = None) -> CompletedProcess :
        """
        *Diff Checker*

        Args:
            options:
                str: Options that has to passed [Default: None]

        Usage:
            Git.diff("--staged --stat")

        Returns:
            object: Complete process
        """
        return execute(f"git diff {options}")

    @git_error("Failed to push")
    def push(self,remote: str |None = None,branch: str |None = None) -> CompletedProcess :
        """
        *As the name it pushes commited codes to remote repo*

        Args:
            remote:
                str: The remote you want push. [Exp: origin]
            branch:
                str: I think theres no need to explain this ;)

        Usage:
            Git.push(remote="origin",branch="main")

        Returns:
            object: Complete Process
        """
        if remote is None and branch is None:
            return execute("git push")
        
        if remote is None or branch is None:
            raise GitError("Provide Both (remote & branch) or dont provide any for default remote.branch")
            
        return execute(f"git push {remote} {branch}")

    def is_repo(self) -> bool :
        """
        *This checks either we are inside a git repo or not?*

        Args:
            None

        Usage:
            Git.is_repo()

        Returns:
            bool: True or False
        """
        try:
            res = execute("git rev-parse --is-inside-work-tree")
            return bool(res.stdout)
        except CalledProcessError:
            return False

    @git_error
    def branch(self) -> CompletedProcess:
        """
        *Checkes for current branch*
        Args:
            None
        Usage:
            Git.branch()
        Returns:
            object: Complete Process

        """
        return execute("git branch --show-current")
