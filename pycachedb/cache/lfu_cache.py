from abc import ABC, abstractmethod
from typing import Dict, Union, Optional, Any

from pycachedb.cache.base import Cache
from pycachedb.data_structures.hash_table import HashTable
from pycachedb.data_structures.linked_list import Node, DoublyLinkedList

class LFUCache(Cache):

    def __init__(self,capacity: int = 128) -> None:
        """
        Initializes the Least Frequently Used Cache

        Args:
            capacity: Maximum number of items the cache can hold
        """
        super().__init__(capacity)
        # Creating the Hash Map from key to its value using the HashTable
        self.cache_map = HashTable(size=1024)
        # Creating the Hash Map from key to frequency using the HashTable
        self.frequency_map = HashTable(size=1024)
        # Mapping from frequency to DoublyLinkedList of nodes with that same frequency
        self.frequency_lists: Dict[int, DoublyLinkedList] = {}
        # Mapping from key to individual Node objects
        self.key_to_node_map = HashTable(size=1024)
        # Minimum frequency in the cache
        self.min_frequency = 0

    def get(self, key: Union[str, Any]) -> Any:
        """
        Retrieve an item from the cache and update its frequency

        Args:
            key: The key to retrieve
        """
        try:
            # Trying to get the value, returns None
            value = self.cache_map.get(key)

            # If found, increment frequency
            self._increment_frequency(key)
            return value
        
        except KeyError:
            return None
        
    def put(self, key: Union[str, int], value: Any) -> None:
        """
        Adds or updates an item in the cache.
        
        Args:
            key: The key for the item
            value: The value to be cached
        """
        # If its at capacity and this is a new key, remove the least frequently used
        if self.capacity <= 0:
            return
        
        try:
            # Updating the existing key
            self.cache_map.get(key)
            self.cache_map.set(key,value)
            self._increment_frequency(key)
            return
        
        except KeyError:
            # New Key
            if self.current_size >= self.capacity:
                # Evicting the least frequently used item
                self._evict()

            # Adding the new key with a frequency 1
            if 1 not in self.frequency_lists:
                self.frequency_lists[1] = DoublyLinkedList()
            
            # Adding to frequency 1 list
            self.frequency_lists[1].insert_to_head(key,value)

            # Storing the reference to the nodes
            node = self.frequency_lists[1].head.next
            self.key_to_node_map.set(key, node)

            # Updating minimum frequency
            self.min_frequency = 1
            self.current_size = self.current_size + 1

    def delete(self, key: Union[str,int]) -> bool:
        """
        Removes an item from the cache.
        
        Args:
            key: The key to remove
            
        Returns:
            True if the key was found and removed, False otherwise
        """
        try:
            # Getting the frequency and the node
            frequency = self.frequency_map.get(key)
            node = self.key_to_node_map.get(key)

            # Removing from the frequency list
            self._remove_node_from_list(node, frequency)

            # Removing from the maps
            self.cache_map.delete(key)
            self.frequency_map.delete(key)
            self.key_to_node_map.delete(key)

            # Updating the minimum frequency if needed
            if frequency == self.min_frequency and self.frequency_lists[frequency].size == 0:
                # Finding the next non-empty frequence
                self.min_frequency = 0
                for f in sorted(self.frequency_lists.keys()):
                    if self.frequency_lists[f].size > 0:
                        self.min_frequency = f
                        break

            self.current_size = self.current_size - 1
            return True
        
        except KeyError:
            return False
        
    def clear(self) -> None:
        """Clear all items from the cache"""
        # Reinitializing all data structures
        self.cache_map = HashTable(size=1024)
        self.frequency_map = HashTable(size=1024)
        self.frequency_lists.clear()
        self.key_to_node_map = HashTable(size=1024)
        self.min_frequency = 0
        self.current_size = 0

    def _increment_frequency(self, key: Union[str, int]) -> None:
        """
        Increments the frequency of an item and update its position

        Args:
            key: The key to update
        """
        current_frequency = self.frequency_map.get(key)
        value = self.cache_map.get(key)
        node = self.key_to_node_map.get(key)

        # Removing the node from the frequency linked list
        self._remove_node_from_list(node,current_frequency)

        # Incrementing the frequency
        new_frequency = current_frequency + 1
        self.frequency_map.set(key, new_frequency)

        # Creating the frequency linked list if it doesn't exist
        if new_frequency not in self.frequency_lists:
            self.frequency_lists[new_frequency] = DoublyLinkedList()

        # Adding to the new frequency list 
        self.frequency_lists[new_frequency].insert_to_head(key,value)
        self.key_to_node_map.set(key,self.frequency_lists[new_frequency].head.next)

        # If the older frequency was the minimum and its list is now empty, we must increment the minimum frequency
        if current_frequency == self.min_frequency and self.frequency_lists[current_frequency].size == 0:
            self.min_frequency = new_frequency

            # Finding the true minimum frequency from non empty lists
            for f in sorted(self.frequency_lists.keys()):
                if self.frequency_lists[f].size > 0:
                    self.min_frequency = f
                    break

    def _remove_node_from_list(self, node: Node, frequency: int) -> None:
        """
        Removes a node from its frequency list.
        
        Args:
            node: The node to remove
            freq: The frequency of the node
        """
        # Updating the next and prev pointers to remove the node
        node.prev.next = node.next
        node.next.prev = node.prev
        
        # Disconnecting the node
        node.next = None
        node.prev = None
        
        # Updating the size of the linked list
        self.frequency_lists[frequency].size = self.frequency_lists[frequency].size - 1

    def _evict(self) -> None:
        """Evicts the least frequently used item"""
        if self.min_frequency == 0 or self.current_size == 0:
            return
        
        # Getting the frequency list with minimum frequency
        min_frequency_list = self.frequency_lists[self.min_frequency]

        # Removing the least recently used item from this frequency
        lfu_node = min_frequency_list.delete_at_end()

        if lfu_node and lfu_node.key is not None:
            # Removing the key from the hash maps
            self.cache_map.delete(lfu_node.key)
            self.frequency_map.delete(lfu_node.key)
            self.key_to_node_map.delete(lfu_node.key)

            # If this frequency is now empty, we'll find a new minimum on the next insertion
            if min_frequency_list.size == 0:
                # Finding the next non-empty frequency
                for f in sorted(self.frequency_lists.keys()):
                    if f > self.min_frequency and self.frequency_lists[f].size > 0:
                        self.min_frequency = f
                        break
                else:
                    self.min_frequency = 0

            self.current_size = self.current_size - 1