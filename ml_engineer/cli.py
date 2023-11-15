from pathlib import Path
import sys, os

from argparse import ArgumentParser, FileType

from ml_engineer.core.ai import OpenAI
from ml_engineer.core.engineer import Engineer

def is_dir(path: str) -> Path:
    """Check if path is a directory."""
    if os.path.isdir(path):
        return Path(path)
    elif Path(path).parent.is_dir():
        Path(path).mkdir(parents=True, exist_ok=True)
        return Path(path)
    else:
        raise NotADirectoryError(path)

def cli(*args):
    parser =ArgumentParser()
    parser.add_argument("input", type=FileType('r'), help="Path to the prompt file")
    parser.add_argument("output", type=is_dir, help="Path to the output directory")
    
    parser.add_argument("--model", type=str, default="gpt35", help="The engine to use for the completion")
    return parser.parse_args(args)

if __name__ == "__main__":
    config = cli(*sys.argv[1:])
    ai = OpenAI(model=config.model)
    do_engineering = Engineer(config.input.read(), config.output, ai)
    do_engineering()
