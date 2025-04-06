from abc import ABC, abstractmethod
from typing import Union, Any

class Cache(ABC):

    def __init__(self, capacity: int = 128) -> None:
        """
        Initializes the cache with a given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.current_size = 0

    @abstractmethod
    def get(self, key: Union[int,str]) -> Any:
        """
        Retrieves an item from the cache.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or None if not found
        """
        pass

    @abstractmethod
    def put(self, key: Union[int, str], value: Any) -> None:
        """
        Adds an item to the cache.
        
        Args:
            key: The key for the item
            value: The value to be cached
        """
        pass

    @abstractmethod
    def delete(self, key: Union[int, str]) -> None:
        """
        Deletes an item from the cache.
        
        Args:
            key: The key to remove
            
        Returns:
            True if the key was found and removed, False otherwise
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears all items from the cache.
        """
        pass