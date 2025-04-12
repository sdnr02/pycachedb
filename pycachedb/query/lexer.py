from enum import Enum
from typing import List, Optional

class TokenType(Enum):
    
    """Enum class representing different types of tokens in the query language"""
    COMMAND = 1
    IDENTIFIER = 2
    STRING = 3
    NUMBER = 4
    FLAG = 5
    END = 6


class Token:
    
    def __init__(
        self,
        token_type: TokenType,
        value: str,
        position: int
    ) -> None:
        """
        Initializes an object of the token class

        Args:
            token_type: TokenType -> The type of this token
            value: str -> The string value of this token
            position: int -> The position in the original query where this token starts
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __str__(self) -> str:
        return f"Token({self.type}, '{self.value}', pos={self.position})"
    
    def __repr__(self) -> str:
        return self.__str__()