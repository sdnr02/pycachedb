from abc import ABC, abstractmethod
from typing import Union, Any, Dict

from pycachedb.cache.base import Cache
from pycachedb.data_structures.hash_table import HashTable
from pycachedb.data_structures.linked_list import Node, DoublyLinkedList

class LRUCache(Cache):

    def __init__(self, capacity: int = 128) -> None:
        """
        Initializes the LRU cache.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        super().__init__(capacity)
        # Intializing the DoublyLinkedList object
        self.dll = DoublyLinkedList()
        # Creating a hash map that maps key value to the next node by initializing the Hash Table class
        self.cache_map = HashTable(size=1024)

    def get(self, key: Union[int, str]) -> Any:
        """
        Retrieves an item from the cache and update its position to be the most recently used.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key, or None if not found
        """
        try:
            # Trying to retrieve the node from the hash map
            node = self.cache_map.get(key)
            value = node.value

            self._remove_node(node)

            # Adding it back to the head position in the list
            self.dll.insert_to_head(key,value)

            # Updating the reference in the hash table
            self.cache_map.set(key,self.dll.head.next)

            return value
        
        except KeyError:
            return None
    
    def put(self, key: Union[int, str], value: Any) -> None:
        """
        Adds or updates an item in the cache.
        
        Args:
            key: The key for the item
            value: The value to be cached
        """

        # Adding an early return if capacity is zero and it's a new key
        if self.capacity == 0:
            try:
                node = self.cache_map.get(key)
                # If this key exists we must remove it
                self._remove_node(node)
                return
            except KeyError:
                # If the key doesn't exist, we shouldn't add it since capacity is zero
                return

        try:        
            # If the key exists, we need to update its value and move it to the front
            node = self.cache_map.get(key)
            self._remove_node(node)
            self.dll.insert_to_head(key,value)
            self.cache_map.set(key, self.dll.head.next)
            return

        except KeyError:
            # If the key doesn't exist, we continue with the insertion process
            pass

        # Checking the capacity and evicting the oldest node
        if self.current_size >= self.capacity:
            lru_node = self.dll.delete_at_end()
            if lru_node and lru_node.key is not None:
                self.cache_map.delete(lru_node.key)
                self.current_size = self.current_size - 1

        # Adding the new item to the head (most recently used)
        self.dll.insert_to_head(key,value)
        self.cache_map.set(key,self.dll.head.next)
        self.current_size = self.current_size + 1

    def delete(self, key: Union[int, str]) -> bool:
        """
        Removes an item from the cache

        Args:
            key: The key to remove

        Returns:
            True if the key was found and retrieved, False otherwise
        """
        try:
            node = self.cache_map.get(key)
            self._remove_node(node)
            self.cache_map.delete(key)
            self.current_size = self.current_size - 1
            return True

        except KeyError:
            return False
    
    def clear(self) -> None:
        """Clears all items from the cache"""
        self.dll = DoublyLinkedList()
        self.cache_map = HashTable(size=1024)
        self.current_size = 0

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
        self.dll.size = self.dll.size - 1
