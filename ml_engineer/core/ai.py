from abc import ABC
from typing import List

import backoff

from openai import AzureOpenAI, RateLimitError


class AI(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.chat_history = []
    
    def add_human_input(self, content: str) -> None:
        """
        This method is intended to add human input to the chat history.

        Args:
            human_input (str): The human input to be added to the chat history.
        """
        self.add_to_history(content, "human")
        
    def add_ai_response(self, content: str) -> None:
        """
        This method is intended to add AI response to the chat history.

        Args:
            ai_response (str): The AI response to be added to the chat history.
        """
        self.add_to_history(content, "assistant")
    
    def add_system_message(self, content: str) -> None:
        """
        This method is intended to add system message to the chat history.

        Args:
            system_message (str): The system message to be added to the chat history.
        """
        self.add_to_history(content, "system")
        
    def clear_history(self) -> None:
        """
        This method is intended to clear the chat history.
        """
        self.chat_history = []
    
    def add_to_history(self, content: str, role: str) -> None:
        """
        This method is intended to add a message to the chat history.

        Args:
            content (str): The message to be added to the chat history.
            role (str): The role of the message to be added to the chat history.
        """
        self.chat_history.append({"role": role, "content": content})
    
    def completion(self, system: str, user: str) -> str:
        """
        This method is intended to generate a completion for a given prompt.

        Args:
            prompt (str): The input string based on which the completion is to be generated.

        Raises:
            NotImplementedError: This is an abstract method that needs to be implemented in a subclass.

        Returns:
            str: The generated completion for the given prompt.
        """
        raise NotImplementedError
    
    def embedding(self, text: str) -> List[float]:
        """
        This method is intended to generate an embedding for a given text.

        Args:
            text (str): The input string based on which the embedding is to be generated.

        Raises:
            NotImplementedError: This is an abstract method that needs to be implemented in a subclass.

        Returns:
            List[float]: The generated embedding for the given text.
        """
        raise NotImplementedError


class OpenAI(AI):
    def __init__(self, model: str = "gpt35") -> None:
        super().__init__()
        self.client = AzureOpenAI(
            api_version="2023-05-15"
        )
        self.model = model
    
    @backoff.on_exception(backoff.expo, RateLimitError)
    def completion(self, system: str, user: str, model: str = None) -> str:
        messages = [
            { "role": "system", "content": system },
            { "role": "user", "content": user }
        ]
        completion = self.client.chat.completions.create(model=self.model if not model else model, messages=messages)
        return completion.choices[0].message.content
    
    @backoff.on_exception(backoff.expo, RateLimitError)
    def embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        embedding = self.client.embedding.create(input = [text], model=model)['data'][0]['embedding']

        return embedding