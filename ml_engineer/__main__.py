import sys
from ml_engineer.cli import cli

from ml_engineer.core.ai import OpenAI
from ml_engineer.core.engineer import Engineer

if __name__ == "__main__":
    config = cli(*sys.argv[1:])
    ai = OpenAI(model=config.model)
    do_engineering = Engineer(config.input.read(), config.output, ai)
    do_engineering()