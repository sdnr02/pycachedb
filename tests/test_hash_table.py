import unittest
from pycachedb.data_structures.hash_table import HashTable

class TestHashTable(unittest.TestCase):

    def setUp(self):
        """Creating a fresh hash table for each test"""
        self.hash_table = HashTable(10)
        
    def test_init(self):
        """Testing that the hash table initializes correctly"""
        self.assertEqual(self.hash_table.size, 10)
        self.assertEqual(len(self.hash_table.buckets), 10)
        for bucket in self.hash_table.buckets:
            self.assertEqual(len(bucket), 0)
            
    def test_hash_int(self):
        """Testing the hash function with integer keys"""
        key = 42
        hash_value = self.hash_table._hash(key)
        self.assertEqual(hash_value, 2)
        
    def test_hash_str(self):
        """Testing the hash function with string keys"""
        key = "test"
        hash_value = self.hash_table._hash(key)
        self.assertIsInstance(hash_value, int)
        self.assertTrue(0 <= hash_value < self.hash_table.size)
        
    def test_set_new_key(self):
        """Testing setting a new key-value pair"""
        self.hash_table.set("name", "John")
        hashed_key = self.hash_table._hash("name")
        bucket = self.hash_table.buckets[hashed_key]
        self.assertEqual(len(bucket), 1)
        self.assertEqual(bucket[0][0], "name")
        self.assertEqual(bucket[0][1], "John")
        
    def test_set_existing_key(self):
        """Testing updating an existing key"""
        self.hash_table.set("name", "John")
        self.hash_table.set("name", "Jane")
        hashed_key = self.hash_table._hash("name")
        bucket = self.hash_table.buckets[hashed_key]
        self.assertEqual(len(bucket), 1)
        self.assertEqual(bucket[0][1], "Jane")
        
    def test_get_existing_key(self):
        """Testing getting a value for an existing key"""
        self.hash_table.set("name", "John")
        value = self.hash_table.get("name")
        self.assertEqual(value, "John")
        
    def test_get_nonexistent_key(self):
        """Testing that getting a nonexistent key raises KeyError"""
        with self.assertRaises(KeyError):
            self.hash_table.get("nonexistent")
            
    def test_delete_existing_key(self):
        """Testing deleting an existing key"""
        self.hash_table.set("name", "John")
        self.hash_table.delete("name")
        hashed_key = self.hash_table._hash("name")
        bucket = self.hash_table.buckets[hashed_key]
        self.assertEqual(len(bucket), 0)
        
    def test_delete_nonexistent_key(self):
        """Testing that deleting a nonexistent key raises KeyError"""
        with self.assertRaises(KeyError):
            self.hash_table.delete("nonexistent")
            
    def test_resize(self):
        """Testing resizing the hash table"""
        # Adding some items
        self.hash_table.set("name", "John")
        self.hash_table.set("age", 30)
        self.hash_table.set("city", "New York")
        
        # Dynamically resizing the table
        self.hash_table.resize(20)
        
        # Checking new size
        self.assertEqual(self.hash_table.size, 20)
        self.assertEqual(len(self.hash_table.buckets), 20)
        
        # Checking that all items are still accessible
        self.assertEqual(self.hash_table.get("name"), "John")
        self.assertEqual(self.hash_table.get("age"), 30)
        self.assertEqual(self.hash_table.get("city"), "New York")
        
    def test_resize_default(self):
        """Testing that resizing with default value works"""
        self.hash_table.resize()
        self.assertEqual(self.hash_table.size, 20)
        
    def test_str(self):
        """Testing the string representation"""
        self.hash_table.set("name", "John")
        string_repr = str(self.hash_table)
        self.assertIn("Hash Table:", string_repr)
        self.assertIn("Key: name", string_repr)
        self.assertIn("Value: John", string_repr)


if __name__ == "__main__":
    unittest.main()