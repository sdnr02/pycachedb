from typing import List, Dict, Any, Optional, Union, Callable, Type
from abc import ABC, abstractmethod

class Command(ABC):

    name: str = ""
    min_args: int = 0
    max_args: Optional[int] = None
    description: str = ""

    def __init__(self, db):
        """Initializes with a reference to the database"""
        self.db = db

    @abstractmethod
    def execute(self, args: List[str]) -> str:
        """Executes the command with the given arguments"""
        pass

    def validate_args(self, args: List[str]) -> Optional[str]:
        """
        Validates the number of arguments.

        Args:
            args: List -> List with the arguments for the command
        
        Returns:
            None if valid, error message if invalid
        """
        if len(args) < self.min_args:
            return f"ERROR: {self.name} command requires at least {self.min_args} argument(s)"
        
        if self.max_args is not None and len(args) > self.max_args:
            return f"ERROR: {self.name} command takes at most {self.max_args} argument(s)"
        
        return None