# ML Engineer

This project aims to simplify and or create code just by using natural language

## Run instructions

```sh
pip install -r requirements.txt
```

```sh
export AZURE_OPENAI_ENDPOINT="https://XXXXXXXXXXXXXXX.openai.azure.com/"
export OPENAI_API_VERSION="2023-05-15"
export AZURE_OPENAI_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

```sh
# Create a file with your basic program instructions with any name. Example, Create a file called "tictactoe.prompt" in current folder with the content.

"
You are going to build a multi-player ticktactoe game where users will alternate turns and play game.
Use any technology you deem required for the project.
"
```

```sh
# python -m ml_engineer.cli <FILEPATH_TO_PROMPT> <FOLDER_TO_CREATE_CODE>

python -m ml_engineer.cli tictactoe.prompt /tmp/tick-tac-toe
```