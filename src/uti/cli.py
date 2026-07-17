"""Import Required dependencies"""
import sys
import click
from .tools import gitpush as gp

@click.group()
def cli():
    """Declare Entry Point Group"""

@cli.command(help="It automates git add -> push workflow")
@click.option('--yolo','-y',is_flag=True)
def gpush(yolo):
    if yolo:
        config = gp.YOLO
    else:
        config = gp.NORMAL
    gp.push(config=config)

def main():
    """Main Entry Point"""
    cli()

if __name__ == '__main__':
    main()
