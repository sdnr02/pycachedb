from typing import  Union, Optional, Any

class Node:

    def __init__(
        self,
        key: Optional[Union[int,str]] = None,
        value: Optional[Any] = None
    ) -> None:
        """
        Initializing the Node class for a doubly linked list, storing key-value pairs for the cache
        
        Args:
            key: str -> The key for the value that requires to be stored
            value: str -> The value related to the key that needs to be stored
        """
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    
    def __init__(self) -> None:
        """
        Intializing the doubly linked list implementation with dummy head and tail nodes.
        
        Args:
            None
        """
        # Create dummy head and tail while initializing
        self.head = Node()
        self.tail = Node()

        # Connecting the head and the tail
        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0


    def insert_to_head(
        self,
        key: Union[int,str],
        value: Any
    ) -> None:
        """
        Adding a node right after the head
        
        Args:
            key: int or str -> Key for the node that needs to be added
            value: Any -> Value that needs to be stored for the appropriate key
        """
        node = Node(key=key,value=value)

        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

        self.size = self.size + 1


    def insert_to_tail(
        self,
        key: Union[int,str],
        value: Any
    ) -> None:
        """
        Adding a node right before the tail
        
        Args:
            key: int or str -> Key for the node that needs to be added
            value: Any -> Value that needs to be stored for the appropriate key
        """
        node = Node(key=key,value=value)
        
        node.next = self.tail
        node.prev = self.tail.prev
        
        self.tail.prev.next = node
        self.tail.prev = node
        
        self.size += 1


    def delete_from_head(self):
        """
        Remove and return the node right after the head.
        
        Args:
            None
        Returns:
            Node: The removed node, or None if list is empty
        """

        if self.head.next == self.tail:
            return None
        
        node_to_remove = self.head.next
        
        self.head.next = node_to_remove.next
        node_to_remove.next.prev = self.head

        node_to_remove.next = None
        node_to_remove.prev = None
        
        self.size -= 1
        return node_to_remove


    def delete_at_end(self):
        """
        Remove and return the node right before the tail.
        
        Args:
            None
        Returns:
            Node: The removed node, or None if list is empty
        """
        if self.tail.prev == self.head:
            return None

        node_to_remove = self.tail.prev
        
        node_to_remove.prev.next = self.tail
        self.tail.prev = node_to_remove.prev
        
        node_to_remove.next = None
        node_to_remove.prev = None
        
        self.size -= 1
        return node_to_remove

    
    def __str__(self):
        if self.size == 0:
            print("The list is empty")
            return ""
        
        result = ""
        n = self.head.next
        while n != self.tail:
            result += f"Key: {n.key}, Value: {n.value}\n"
            n = n.next
        
        return result