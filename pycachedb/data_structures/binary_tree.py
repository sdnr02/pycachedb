from typing import Union, Any, Optional

class TreeNode:

    def __init__(
        self,
        key: Union[int,str],
        value: Any,
        left: Any = None,
        right: Any = None
    ) -> None:
        """
        Initialize a tree node with key, value, and optional left and right children.
        
        Args:
            key: The key used for ordering and lookup
            value: The value associated with the key
            left: Left child node (optional)
            right: Right child node (optional)
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"TreeNode(key={self.key}, value={self.value})"
    

class BinaryTree:

    def __init__(
        self,
        root: Optional[TreeNode] = None
    ) -> None:
        self.root = root
        self.size = 0


    def insert(
        self,
        key: Union[int, str],
        value: Any
    ) -> None:
        """
        Inserting a key-value pair into the tree.
        
        Args:
            key: The key to insert
            value: The value to associate with the key
        """
        if self.root is None:
            self.root = TreeNode(key, value)
            self.size = 1
            return
        
        self._insert_recursive(self.root, key, value)
    

    def _insert_recursive(
        self,
        node: TreeNode,
        key: Union[str, Any],
        value: Any
    ) -> None:
        """
        Recursively inserts a node into the tree.
        
        Args:
            node: The current node in the recursion
            key: The key to insert
            value: The value to associate with the key
            
        Returns:
            The subtree root after insertion
        """
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)

        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)

        else:
            node.value = value
        
        return node
    

    def search(
        self,
        key: Union[str, Any]
    ) -> Optional[Any]:
        """
        Searches for a value by its key.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        node = self._search_recursive(self.root, key)
        
        if node:
            return node.value
        
        else:
            None

    
    def _search_recursive(
        self,
        node: Optional[TreeNode],
        key: Union[int,str]
    ) -> Optional[TreeNode]:
        """
        Recursively searches the tree for a key.
        
        Args:
            node: The current node in the recursion
            key: The key to search for
            
        Returns:
            The node containing the key, or None if not found
        """
        if node is None:
            return None

        if key == node.key:
            return node
        
        elif key < node.key:
            return self._search_recursive(node.left, key)
        
        else:
            return self._search_recursive(node.right, key)
        
    
    def delete(self, key: Any) -> bool:
        """
        Deletes a node with the given key from the tree.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        if not self._search_recursive(self.root, key):
            return False
        
        self.root = self._delete_recursive(self.root, key)
        self.size -= 1
        return True
    
    def _delete_recursive(
        self, 
        node: Optional[TreeNode], 
        key: Any
    ) -> Optional[TreeNode]:
        """
        Recursively deletes a node from the tree.
        
        Args:
            node: The current node in the recursion
            key: The key to delete
            
        Returns:
            The subtree root after deletion
        """
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:          
            # Case 1: Node with no children or one child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Case 2: Node with two children
            # Find the inorder successor (smallest node in right subtree)
            successor = self._find_min(node.right)
            
            # Copy successor key and value to this node
            node.key = successor.key
            node.value = successor.value
            
            # Delete the successor
            node.right = self._delete_recursive(node.right, successor.key)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """
        Find the node with the minimum key in the subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum key
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def clear(self) -> None:
        """
        Clear the tree.
        """
        self.root = None
        self.size = 0