from pathlib import Path


class ProjectFS:
    def __init__(self, root: Path) -> None:
        self.root = root
    
    def write_file(self, filename: str, content: str) -> None:
        """
        This method is intended to write content to a file.

        Args:
            path (Path): The path to the file to be written.
            content (str): The content to be written to the file.
        """
        if not self.root.joinpath(filename).exists():
            self.root.joinpath(filename).parent.mkdir(parents=True, exist_ok=True)
            
        self.root.joinpath(filename).write_text(content)