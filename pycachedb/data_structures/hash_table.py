from typing import List, Dict, Optional, Any, Union

class HashTable:

    def __init__(self, size: int) -> None:
        """
        Initializing the hash table with the size of the hash table that needs to be created,
        the initialization process then calls a function that creates a list of lists that will act as the buckets.
        Buckets contain all information regarding the key that it is mapped to.

        Args:
            size: int -> This is the size of the hash table

        Returns:
            None
        """

        self.size = size
        self.buckets = self._create_buckets()

    def _create_buckets(self) -> List:
        """
        Creates an empty list of buckets that we will use as base for the hash table in the future

        Args:
            size: int -> Required number of buckets

        Returns:
            List -> List of buckets of size that was required
        """

        bucket_list = []
        for _ in range(0, self.size-1):
            bucket_list.append([])

        return bucket_list
    
    def _hash(self, key: Union[str,int]) -> int:
        """
        Custom hash function that we will leverage

        Args:
            key: str or int -> The key that we need to hash

        Returns:
            int: the value of the hash
        """

        hash_key = None

        if isinstance(key, int):
            hash_key = key % (self.size)

        elif isinstance(key, str):
            char_list = []
            for character in key:
                if character != ' ':
                    char_list.append(str(ord(character)))
            ascii_number = int(''.join(char_list))
            
            hash_key = ascii_number % self.size

        else:
            raise TypeError("CRITCAL ERROR: Hashing attempted on value that is not : {str or float}")

        return hash_key
    
    def test_hash(self, key: Union[str, int]) -> int:
        return self._hash(key)