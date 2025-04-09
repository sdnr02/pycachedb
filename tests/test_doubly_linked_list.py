import unittest
from typing import Union, Optional, Any

from pycachedb.data_structures.linked_list import Node, DoublyLinkedList

class TestNode(unittest.TestCase):
    """Test cases for the Node class"""
    
    def test_node_initialization(self):
        """Test that a Node is properly initialized with key and value"""
        node = Node(key="test_key", value="test_value")
        self.assertEqual(node.key, "test_key")
        self.assertEqual(node.value, "test_value")
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)
    
    def test_node_empty_initialization(self):
        """Test that a Node can be initialized without key and value"""
        node = Node()
        self.assertIsNone(node.key)
        self.assertIsNone(node.value)
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)


class TestDoublyLinkedList(unittest.TestCase):
    """Test cases for the DoublyLinkedList class"""
    
    def setUp(self):
        """Set up a new DoublyLinkedList for each test"""
        self.dll = DoublyLinkedList()
    
    def test_initialization(self):
        """Test that a DoublyLinkedList is properly initialized"""
        self.assertEqual(self.dll.size, 0)
        self.assertIsNotNone(self.dll.head)
        self.assertIsNotNone(self.dll.tail)
        self.assertEqual(self.dll.head.next, self.dll.tail)
        self.assertEqual(self.dll.tail.prev, self.dll.head)
    
    def test_insert_to_head_empty_list(self):
        """Test insert_to_head on an empty list"""
        self.dll.insert_to_head("key1", "value1")
        self.assertEqual(self.dll.size, 1)
        self.assertEqual(self.dll.head.next.key, "key1")
        self.assertEqual(self.dll.head.next.value, "value1")
        self.assertEqual(self.dll.tail.prev.key, "key1")
        self.assertEqual(self.dll.tail.prev.value, "value1")
    
    def test_insert_to_head_non_empty_list(self):
        """Test insert_to_head on a non-empty list"""
        self.dll.insert_to_head("key1", "value1")
        self.dll.insert_to_head("key2", "value2")
        self.assertEqual(self.dll.size, 2)
        self.assertEqual(self.dll.head.next.key, "key2")
        self.assertEqual(self.dll.head.next.value, "value2")
        self.assertEqual(self.dll.head.next.next.key, "key1")
        self.assertEqual(self.dll.head.next.next.value, "value1")
    
    def test_insert_to_tail_empty_list(self):
        """Test insert_to_tail on an empty list"""
        self.dll.insert_to_tail("key1", "value1")
        self.assertEqual(self.dll.size, 1)
        self.assertEqual(self.dll.head.next.key, "key1")
        self.assertEqual(self.dll.head.next.value, "value1")
        self.assertEqual(self.dll.tail.prev.key, "key1")
        self.assertEqual(self.dll.tail.prev.value, "value1")
    
    def test_insert_to_tail_non_empty_list(self):
        """Test insert_to_tail on a non-empty list"""
        self.dll.insert_to_tail("key1", "value1")
        self.dll.insert_to_tail("key2", "value2")
        self.assertEqual(self.dll.size, 2)
        self.assertEqual(self.dll.tail.prev.key, "key2")
        self.assertEqual(self.dll.tail.prev.value, "value2")
        self.assertEqual(self.dll.tail.prev.prev.key, "key1")
        self.assertEqual(self.dll.tail.prev.prev.value, "value1")
    
    def test_delete_from_head_empty_list(self):
        """Test delete_from_head on an empty list"""
        node = self.dll.delete_from_head()
        self.assertIsNone(node)
        self.assertEqual(self.dll.size, 0)
    
    def test_delete_from_head_single_element(self):
        """Test delete_from_head on a list with a single element"""
        self.dll.insert_to_head("key1", "value1")
        node = self.dll.delete_from_head()
        self.assertEqual(node.key, "key1")
        self.assertEqual(node.value, "value1")
        self.assertEqual(self.dll.size, 0)
        self.assertEqual(self.dll.head.next, self.dll.tail)
        self.assertEqual(self.dll.tail.prev, self.dll.head)
    
    def test_delete_from_head_multiple_elements(self):
        """Test delete_from_head on a list with multiple elements"""
        self.dll.insert_to_head("key1", "value1")
        self.dll.insert_to_head("key2", "value2")
        node = self.dll.delete_from_head()
        self.assertEqual(node.key, "key2")
        self.assertEqual(node.value, "value2")
        self.assertEqual(self.dll.size, 1)
        self.assertEqual(self.dll.head.next.key, "key1")
        self.assertEqual(self.dll.head.next.value, "value1")
    
    def test_delete_at_end_empty_list(self):
        """Test delete_at_end on an empty list"""
        node = self.dll.delete_at_end()
        self.assertIsNone(node)
        self.assertEqual(self.dll.size, 0)
    
    def test_delete_at_end_single_element(self):
        """Test delete_at_end on a list with a single element"""
        self.dll.insert_to_tail("key1", "value1")
        node = self.dll.delete_at_end()
        self.assertEqual(node.key, "key1")
        self.assertEqual(node.value, "value1")
        self.assertEqual(self.dll.size, 0)
        self.assertEqual(self.dll.head.next, self.dll.tail)
        self.assertEqual(self.dll.tail.prev, self.dll.head)
    
    def test_delete_at_end_multiple_elements(self):
        """Test delete_at_end on a list with multiple elements"""
        self.dll.insert_to_tail("key1", "value1")
        self.dll.insert_to_tail("key2", "value2")
        node = self.dll.delete_at_end()
        self.assertEqual(node.key, "key2")
        self.assertEqual(node.value, "value2")
        self.assertEqual(self.dll.size, 1)
        self.assertEqual(self.dll.tail.prev.key, "key1")
        self.assertEqual(self.dll.tail.prev.value, "value1")
    
    def test_mixed_operations(self):
        """Test a mix of operations to ensure correct behavior"""
        self.dll.insert_to_head("key1", "value1")
        self.dll.insert_to_tail("key2", "value2")
        self.dll.insert_to_head("key3", "value3")
    
        self.assertEqual(self.dll.size, 3)
        self.assertEqual(self.dll.head.next.key, "key3")
        self.assertEqual(self.dll.tail.prev.key, "key2")
        
        node = self.dll.delete_from_head()
        self.assertEqual(node.key, "key3")
        self.assertEqual(self.dll.size, 2)
        
        node = self.dll.delete_at_end()
        self.assertEqual(node.key, "key2")
        self.assertEqual(self.dll.size, 1)
    
        self.assertEqual(self.dll.head.next.key, "key1")
        self.assertEqual(self.dll.tail.prev.key, "key1")
    
    def test_int_keys(self):
        """Test that the list works with integer keys"""
        self.dll.insert_to_head(1, "value1")
        self.dll.insert_to_tail(2, "value2")
        self.assertEqual(self.dll.head.next.key, 1)
        self.assertEqual(self.dll.tail.prev.key, 2)
    
    def test_str_representation(self):
        """Test the string representation of the list"""
        # Empty list
        self.assertEqual(self.dll.__str__(), "")
        
        # Non-empty list
        self.dll.insert_to_head("key1", "value1")
        self.dll.insert_to_tail("key2", "value2")
        expected_str = "Key: key1, Value: value1\nKey: key2, Value: value2\n"
        self.assertEqual(self.dll.__str__(), expected_str)


if __name__ == "__main__":
    unittest.main()