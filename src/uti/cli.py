"""Import Required dependencies"""
import sys
import click
from .tools import gitpush as gp
from .tools.formattexts import (readmd)


@click.group()
def cli():
    """Declare Entry Point Group"""

@cli.command(help="It automates git add -> push workflow")
@click.option('--yolo','-y',is_flag=True)
def gpush(yolo):
    """
    *The git add -> git push automater with AI suggested commit message*
    Args:
        None
    
    Usage:
        $ uti gpush {/ for interective mode }
                OR
        $ uti gpush -y / --yolo {/ for less permission *USE WITH CAUTION* }
    
    /* WHY: While doing const commits sometimes our minds get blank; 
    like "What to write now T_T " so this helps with that. */
    """
    if yolo:
        config = gp.YOLO
    else:
        config = gp.NORMAL
    gp.push(config=config)

@cli.group()
def format():
    """
    *The text formatting group*
    [This group contains formatting for diff langs]

    Args:
        None

    Usage:
        $ cat <file-name> | uti format <sub_cmd-acrdng-to-lang>

    Returns:
        FormattedText: Prints out Formatted Text mostly using python.rich.console
    
    /* WHY: Instead of downloading 100s' of tools just to format text. This sloves all into one cmd and low dependency
    (python.rich) mainly */
    """

@format.command(help="This is for formatting Markdown!")
def md():
    """
    *The Text Formatting for Markdown*
    [This method is for formatting Markdown Texts]

    Args:
        None
    
    Usage:
        $ cat <file-name>.md | uti format md
    
    Retruns:
        MarkDown: Prints out Markdown formatted text using rich.markdown
    
    /* WHY: The glo Takes so much startup time than python.rich */
    """
    readmd.main()

def main():
    cli()

if __name__ == '__main__':
    cli()
