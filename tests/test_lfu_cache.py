import unittest
from typing import Union, Any, Dict

from pycachedb.cache.lfu_cache import LFUCache

class TestLFUCache(unittest.TestCase):
    """Test cases for the LFUCache class"""
    
    def setUp(self):
        """Set up a new LFUCache for each test"""
        self.cache = LFUCache(capacity=3)
    
    def test_initialization(self):
        """Test that a LFUCache is properly initialized"""
        self.assertEqual(self.cache.capacity, 3)
        self.assertEqual(self.cache.current_size, 0)
        self.assertEqual(self.cache.min_frequency, 0)
        self.assertEqual(len(self.cache.frequency_lists), 0)
    
    def test_put_get_basic(self):
        """Test basic put and get operations"""
        self.cache.put("key1", "value1")
        
        self.assertEqual(self.cache.current_size, 1)
        self.assertEqual(self.cache.min_frequency, 1)

        value = self.cache.get("key1")
        self.assertEqual(value, "value1")
        
        frequency = self.cache.frequency_map.get("key1")
        self.assertEqual(frequency, 2)
    
    def test_put_update_existing(self):
        """Test updating an existing key"""
        self.cache.put("key1", "value1")
        
        self.cache.put("key1", "updated_value")
        self.assertEqual(self.cache.current_size, 1)
        
        value = self.cache.get("key1")
        self.assertEqual(value, "updated_value")

        frequency = self.cache.frequency_map.get("key1")
        self.assertEqual(frequency, 3)
    
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
        self.assertEqual(self.cache.min_frequency, 0)
        self.assertEqual(len(self.cache.frequency_lists), 0)

        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
    
    def test_lfu_eviction_same_frequency(self):
        """Test that when multiple items have the same frequency, the least recently used one is evicted"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        
        self.cache.put("key4", "value4")

        self.assertIsNone(self.cache.get("key1"))
        
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
    
    def test_lfu_eviction_different_frequencies(self):
        """Test that the least frequently used item is evicted when the cache is full"""
        self.cache.put("key1", "value1")
        self.cache.get("key1")
        self.cache.get("key1")
        
        self.cache.put("key2", "value2")
        self.cache.get("key2")

        self.cache.put("key3", "value3")
        
        self.cache.put("key4", "value4")

        self.assertIsNone(self.cache.get("key3"))

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key4"), "value4")
    
    def test_frequency_tracking(self):
        """Test that frequencies are tracked correctly"""
        self.cache.put("key1", "value1")
        self.cache.get("key1")
        self.cache.get("key1")
        
        self.assertEqual(self.cache.frequency_map.get("key1"), 3)
        self.cache.put("key1", "updated_value")
        
        self.assertEqual(self.cache.frequency_map.get("key1"), 4)
    
    def test_min_frequency_update(self):
        """Test that the minimum frequency is updated correctly"""
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.min_frequency, 1)
        
        self.cache.get("key1")
        self.assertEqual(self.cache.min_frequency, 2)
        
        self.cache.put("key2", "value2")
        self.assertEqual(self.cache.min_frequency, 1)
    
    def test_zero_capacity(self):
        """Test behavior with zero capacity"""
        zero_cache = LFUCache(capacity=0)

        zero_cache.put("key1", "value1")
        
        self.assertEqual(zero_cache.current_size, 0)
        self.assertIsNone(zero_cache.get("key1"))
    
    def test_negative_capacity(self):
        """Test behavior with negative capacity (should be treated as zero)"""
        negative_cache = LFUCache(capacity=-5)

        negative_cache.put("key1", "value1")
        
        self.assertEqual(negative_cache.current_size, 0)
        self.assertIsNone(negative_cache.get("key1"))
    
    def test_mixed_key_types(self):
        """Test that the cache works with different key types"""
        self.cache.put(1, "value1")
        self.cache.put("key2", "value2")
        
        self.assertEqual(self.cache.get(1), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")


if __name__ == "__main__":
    unittest.main()