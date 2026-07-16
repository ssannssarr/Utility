"""Import Required dependencies"""
import sys
from .tools.gitpush import (
    push,
    YOLO,
    NORMAL
)

def main():
    """Main Entry Point"""
    if sys.argv[1] in ('-y',):
        config = YOLO
    else:
        config = NORMAL

    push(config=config)

if __name__ == '__main__':
    main()
