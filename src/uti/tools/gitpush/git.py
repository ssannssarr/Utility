"""Import Required Dependencies"""
import subprocess as sp

def run(cmd: str) -> str:
    """Runs an Cmd and returns"""
    return sp.run(
        cmd,
        check=True,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

class Git:
    """Git helper Class"""
    def add(self,files: str):
        """
        *Adds passed files*

        Args:
            files: (you can use options also though XD)
                File names that you will add

        Usage:
            Git.add("-A")

        Returns:
            None
        """
        run(f"git add {files}")

    def commit(self,msg: str) -> str:
        """
        *Commits staged files*
        
        Args:
            msg: 
                str: The Message for commit (or in simple 'commit message')

        Usage:
            Git.commit("Initail Commit")

        Returns:
            str: The stdout and stderr that comes from running the command 
        """
        res =  run(f"git commit -m {msg}")
        return res.stdout,res.stderr

    def diff(self,options: str = None) -> str:
        """
        *Diff Checker*

        Args:
            options:
                str: Options that has to passed [Default: None]

        Usage:
            Git.diff("--staged --stat")

        Returns:
            str: The stdout and stderr that comes from running the command


        """
        res = run(f"git diff {options}")
        return res.stdout, res.stderr

    def push(self,remote: str = None,branch: str = None):
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
            None
        """
        run(f"git push {remote} {branch}")

    def is_repo(self):
        """
        *This checks either we are inside a git repo or not?*
        
        Args:
            None

        Usage:
            Git.is_repo()

        Returns:
            str: The stdout and stderr that comes from running the command
        """
        res = run("git rev-parse --is-inside-work-tree")
        return res.stdout,res.stderr
