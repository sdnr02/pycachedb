from abc import ABC, abstractmethod
from typing import Union, Any, Dict

from pycachedb.cache.base import Cache
from pycachedb.data_structures.linked_list import Node, DoublyLinkedList

class LRUCache(Cache):

    def __init__(self, capacity: int = 128) -> None:
        """
        Initializes the LRU cache.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        super.__init__(capacity)
        # Intializing the DoublyLinkedList object
        self.dll = DoublyLinkedList()
        # Creating a hash map that maps key value to the next node
        self.cache_map: Dict[Union[int,str],Node] = {}

    def get(self, key: Union[int, str]) -> Any:
        """
        Retrieves an item from the cache and update its position to be the most recently used.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or None if not found
        """
        if key not in self.cache_map:
            return None
        
        # Getting the node and its value if in the hash map
        node = self.cache_map[key]
        value = node.value

        self._remove_node(node)

        # Adding it back to the head position in the list
        self.dll.insert_to_head(key,value)

        self.cache_map[key] = self.dll.head.next

        return value
    
    def put(self, key: Union[int, str], value: Any) -> None:
        """
        Adds or updates an item in the cache.
        
        Args:
            key: The key for the item
            value: The value to be cached
        """

        # If the key exists, we need to update its value and move it to the front
        if key in self.cache_map:
            self._remove_node(self.cache_map[key])
            self.dll.insert_to_head(key,value)
            self.cache_map[key] = self.dll.head.next

        if self.current_size >= self.capacity:
            lru_node = self.dll.delete_at_end()
            if lru_node and lru_node.key is not None:
                del self.cache_map[lru_node.key]
                self.current_size -= 1

        # Adding the new item to the head (most recently used)
        self.dll.insert_to_head(key, value)
        self.cache_map[key] = self.dll.head.next
        self.current_size += 1

    def _remove_node(self, node: Node) -> None:
        """
        Helper method to remove a node from the linked list.
        
        Args:
            node: The node to remove
        """
        # Updating the next and prev pointers to remove the node
        node.prev.next = node.next
        node.next.prev = node.prev
        
        # Disconnecting the node
        node.next = None
        node.prev = None
        
        # Updating the size of the linked list
        self.dll.size -= 1