import re
from pathlib import Path
from typing import Callable
from ml_engineer.core.ai import AI

from ml_engineer.core.projectfs import ProjectFS

class CodeParser:
    def parse(self, code: str):
        pass


class Engineer(Callable):
    def __init__(self, initial_prompt: str, project_directory: Path, ai: AI):
        self.project_scope = initial_prompt
        self.fs = ProjectFS(project_directory)
        self.ai = ai

    def __call__(self, *args, **kwargs):
        print(f"Hello, my name is Dave, I will be working for you today.")
        scope = self.project_scope_discussion()
        code_folder = self.generate_code()
        print(f"Checkout the code at: {code_folder}")
    
    def _history_formatter(self, messages):
        output = "# Clarifications\n"
        for message in messages:
            output += f"{'Q: ' if message['role'] == 'system' else 'A: '}: {message['content']}\n"
        return output
    
    
    def generate_code(self):
        template = Path(__file__).parent.parent.joinpath("prompts", "implementation.jinja2")
        response = self.ai.completion(template.read_text(), self.project_scope)
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    
        blocks = re.finditer(regex, response, re.DOTALL)
        for block in blocks:
            filepath = block.group(1)
            content = block.group(2)
            self.fs.write_file(filepath, content)
        return self.fs.root.as_posix()
        
    
    def update_project_scope(self, scope):
        self.project_scope = scope
    
    def project_scope_discussion(self, messages = []):
        template = Path(__file__).parent.parent.joinpath("prompts", "clarify.jinja2")
        response = self.ai.completion(template.read_text(), self.project_scope)
        while response.lower().strip() != "nothing to clarify.":
            messages.append({"role": "system", "content": response})
            clarification = input(f"Dave: {response}\nYou: ")
            messages.append({"role": "human", "content": clarification})
            new_scope = self.project_scope + self._history_formatter(messages)
            response = self.ai.completion(template.read_text(), new_scope)
            
        scope = self.project_scope + self._history_formatter(messages)
        self.update_project_scope(scope)
        return scope