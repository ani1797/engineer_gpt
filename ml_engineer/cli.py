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

import re

def extract_filename_and_codeblock(markdown_text):
    # Regex pattern for filename
    filename_pattern = r'```markdown\n(.*?)\n```'
    # Regex pattern for code block
    codeblock_pattern = r'```(?:[a-z]+\n)?(.*?)```'

    # Find filename
    filename = re.search(filename_pattern, markdown_text, re.DOTALL)
    filename = filename.group(1) if filename else None

    # Find code block
    codeblock = re.search(codeblock_pattern, markdown_text, re.DOTALL)
    codeblock = codeblock.group(1) if codeblock else None

    return filename, codeblock


if __name__ == "__main__":
    config = cli(*sys.argv[1:])
    ai = OpenAI(model=config.model)
    do_engineering = Engineer(config.input.read(), config.output, ai)
    do_engineering()