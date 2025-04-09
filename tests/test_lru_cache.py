import unittest
from typing import Union, Any, Dict

from pycachedb.cache.lru_cache import LRUCache

class TestLRUCache(unittest.TestCase):
    """Test cases for the LRUCache class"""
    
    def setUp(self):
        """Set up a new LRUCache for each test"""
        self.cache = LRUCache(capacity=3)
    
    def test_initialization(self):
        """Test that a LRUCache is properly initialized"""
        self.assertEqual(self.cache.capacity, 3)
        self.assertEqual(self.cache.current_size, 0)
        self.assertEqual(self.cache.dll.size, 0)
        
    def test_put_get_basic(self):
        """Test basic put and get operations"""
        self.cache.put("key1", "value1")
    
        self.assertEqual(self.cache.current_size, 1)
        self.assertEqual(self.cache.dll.size, 1)

        value = self.cache.get("key1")
        self.assertEqual(value, "value1")
        
    def test_put_update_existing(self):
        """Test updating an existing key"""
        self.cache.put("key1", "value1")
        
        self.cache.put("key1", "updated_value")
        
        self.assertEqual(self.cache.current_size, 1)
        self.assertEqual(self.cache.dll.size, 1)
        
        value = self.cache.get("key1")
        self.assertEqual(value, "updated_value")
        
    def test_get_nonexistent(self):
        """Test getting a nonexistent key"""
        value = self.cache.get("nonexistent_key")
        self.assertIsNone(value)
        
    def test_delete_existing(self):
        """Test deleting an existing key"""
        self.cache.put("key1", "value1")
        
        result = self.cache.delete("key1")
        
        self.assertTrue(result)
        self.assertEqual(self.cache.current_size, 0)
        self.assertEqual(self.cache.dll.size, 0)

        value = self.cache.get("key1")
        self.assertIsNone(value)
        
    def test_delete_nonexistent(self):
        """Test deleting a nonexistent key"""
        result = self.cache.delete("nonexistent_key")
        self.assertFalse(result)
        
    def test_clear(self):
        """Test clearing the cache"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")

        self.cache.clear()

        self.assertEqual(self.cache.current_size, 0)
        self.assertEqual(self.cache.dll.size, 0)

        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
        
    def test_lru_eviction(self):
        """Test that the least recently used item is evicted when the cache is full"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        
        self.assertEqual(self.cache.current_size, 3)
        
        self.cache.put("key4", "value4")
        
        self.assertIsNone(self.cache.get("key1"))
        
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
        
        self.assertEqual(self.cache.current_size, 3)
        
    def test_lru_order_update_on_get(self):
        """Test that the LRU order is updated when an item is accessed"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        
        self.cache.get("key1")
        
        self.cache.put("key4", "value4")
        
        self.assertIsNone(self.cache.get("key2"))
        
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
        
    def test_lru_order_update_on_put(self):
        """Test that the LRU order is updated when an item is updated via put"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        
        self.cache.put("key1", "updated_value")
        self.cache.put("key4", "value4")
        
        self.assertIsNone(self.cache.get("key2"))
        
        self.assertEqual(self.cache.get("key1"), "updated_value")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
        
    def test_mixed_key_types(self):
        """Test that the cache works with different key types"""
        self.cache.put(1, "value1")
        self.cache.put("key2", "value2")
        
        self.assertEqual(self.cache.get(1), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        
    def test_zero_capacity(self):
        """Test behavior with zero capacity"""
        zero_cache = LRUCache(capacity=0)
        
        zero_cache.put("key1", "value1")
        
        self.assertEqual(zero_cache.current_size, 0)
        self.assertIsNone(zero_cache.get("key1"))


if __name__ == "__main__":
    unittest.main()