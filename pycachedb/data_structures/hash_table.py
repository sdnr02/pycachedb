from typing import List, Dict, Optional, Any, Union

class HashTable:
    """
    TODO: Implement auto resizing
    """

    def __init__(self, size: int) -> None:
        """
        Initializing the hash table with the size of the hash table that needs to be created,
        the initialization process then calls a function that creates a list of lists that will act as the buckets.
        Buckets contain all documents.
        Documents are key, value pairs that houses the information required.

        Args:
            size: int -> This is the size of the hash table

        Returns:
            None
        """

        self.size = size
        self.buckets = self._create_buckets()
    
    def __str__(self):
        """What gets printed when we access the hash table in a print function"""
        
        output_list = []
        for index, bucket in enumerate(self.buckets):
            for key, value in bucket:
                output_list.append(f"Bucket {index} -> Key: {key}, Value: {value}")
        
        return "Hash Table:\n"+"\n".join(output_list)

    def _create_buckets(self) -> List:
        """
        Creates an empty list of buckets that we will use as base for the hash table in the future

        Args:
            size: int -> Required number of buckets

        Returns:
            List -> List of buckets of size that was required
        """

        bucket_list = []
        for _ in range(0, self.size):
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
    
    def set(
        self,
        key: Union[str, int],
        value: Any
    ) -> None:
        """
        Function that will help set values into the hash map

        Args:
            key: str or int -> The key that we need to hash
            value: Any -> The value that needs to be added to the bucket of the key

        Returns:
            None -> Only prints a success message if set correctly
        """

        hashed_key = self._hash(key)

        bucket = self.buckets[hashed_key]

        for index, document in enumerate(bucket):
            document_key, _ = document

            if document_key == key:
                bucket[index] = (key, value)
                print("Successfully updated value in the bucket")
                return
                
        bucket.append((key,value))
        print("Successfully added new value to the buckets")

    def get(self, key: Union[str, int]) -> Any:
        """
        Function that will retrieve the value associated with the key from its document in the hash bucket

        Args:
            key: str or int -> The key that we need to hash

        Returns:
            Any -> Value that is mapped to the key in the table
        """

        hashed_key = self._hash(key)

        bucket = self.buckets[hashed_key]

        for document in bucket:
            document_key, document_value = document

            if document_key == key:
                return document_value
            
        raise KeyError("Key not found in the hash table")
    
    def delete(self, key: Union[str, int]) -> None:
        """
        Function to delete the value at a particular key in a hash table

        Args:
            key: str or int -> The key that we need to delete

        Returns:
            None: Prints a success message if the value was deleted successfully
        """

        hashed_key = self._hash(key)

        bucket = self.buckets[hashed_key]

        for index, document in enumerate(bucket):
            document_key, _ = document

            if document_key == key:
                bucket.pop(index)
                print("Successfully deleted key from the hash table")
                return

        raise KeyError("Key not found in hash table for deletion")
    
    def resize(self, new_size: Optional[int] = None) -> None:
        """
        Resizes the hash table to a new size (typically double the current size).
        Rehashes all existing elements into the new buckets.s
        
        Args:
            new_size: Optional[int] -> New size for the hash table. If None, defaults to double the current size.
        
        Returns:
            None: Prints a success message if resizing was successful
        """

        buckets_copy = []
        for bucket in self.buckets:
            for document_key, document_value in bucket:
                buckets_copy.append((document_key, document_value))

        self.size = new_size if new_size else (2*self.size)
        self.buckets = self._create_buckets()

        for document_key, document_value in buckets_copy:
            hashed_key = self._hash(document_key)

            bucket = self.buckets[hashed_key]
            bucket.append((document_key, document_value))

        print("Resizing completed successfully")