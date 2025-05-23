# PyCacheDB: In-Memory Database with Custom Query Language

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)]()

PyCacheDB is a lightweight, in-memory database/cache system with a custom query language, implemented purely in Python. This project aims to provide a Redis-like experience while helping developers understand the underlying data structures and algorithms.

## 🔑 Key Features

- In-memory key-value store with multiple data type support
- Custom query language for data manipulation
- Cache eviction policies (LRU, LFU)
- Optional persistence mechanisms
- Network interface for client-server architecture

## 🚀 Current Progress

- ✅ Core data structures
  - ✅ Hash Table implementation
  - ✅ Binary Tree implementation
  - ✅ Doubly Linked List implementation
- ✅ Caching mechanisms
  - ✅ LRU (Least Recently Used) cache strategy
  - ✅ LFU (Least Frequently Used) cache strategy
- ✅ Query language components
  - ✅ Lexer for tokenizing queries
  - ✅ Command pattern architecture
  - ✅ Parser for executing queries
- ✅ Unit tests for data structures and cache implementations

## 🛠️ Installation

Clone the repository:
```bash
git clone https://github.com/sidnair02/pycachedb.git
cd pycachedb
```

No external dependencies are required as PyCacheDB uses only the Python standard library.

## 🧪 Running Tests

Run all tests using the included batch script from the root directory:

```bash
# On Windows
run_tests.bat
```

## 📝 Usage (coming soon)

```python
from pycachedb import PyCacheDB

# Initialize the database with LRU cache
db = PyCacheDB(eviction_policy="LRU")

# Execute queries using the custom query language
db.execute("SET user:1 'John Doe'")
db.execute("SET user:2 'Jane Smith'")

# Get values
user = db.execute("GET user:1")  # Returns: John Doe

# Delete values
db.execute("DEL user:2")

# Work with lists
db.execute("LPUSH my-list 'item1' 'item2' 'item3'")
items = db.execute("LRANGE my-list 0 -1")  # Returns all items

# Work with hashes
db.execute("HSET user:profile name 'John' age '30' city 'New York'")
city = db.execute("HGET user:profile city")  # Returns: New York

# Use transactions
db.execute("MULTI")
db.execute("SET counter 1")
db.execute("INCR counter")
db.execute("GET counter")
results = db.execute("EXEC")  # Returns: ["OK", "2", "2"]
```

## 🏗️ Project Structure

```
pycachedb/
├── pycachedb/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── lfu_cache.py
│   │   └── lru_cache.py
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── binary_tree.py
│   │   ├── hash_table.py
│   │   └── linked_list.py
│   └── query/
│       ├── __init__.py
│       ├── commands.py
│       ├── lexer.py
│       └── parser.py
├── tests/
│   ├── __init__.py
│   ├── test_doubly_linked_list.py
│   ├── test_hash_table.py
│   ├── test_lfu_cache.py
│   └── test_lru_cache.py
├── run_tests.bat
├── PLAN.md
└── README.md
```

## 📋 Implementation Plan

### Completed
- [x] Core data structures
  - [x] Hash table for key-value storage
  - [x] Binary tree for ordered operations
  - [x] Doubly linked list for caching mechanisms
- [x] Cache eviction policies
  - [x] LRU (Least Recently Used) implementation
  - [x] LFU (Least Frequently Used) implementation
- [x] Query language components
  - [x] Command pattern architecture
  - [x] Lexer for tokenization
  - [x] Parser for command execution

### Next Steps
- [ ] Data types & operations
  - [ ] Complete list operations (LPUSH, RPUSH, etc.)
  - [ ] Complete hash operations (HSET, HGET, etc.)
  - [ ] Implement sorted sets
- [ ] Persistence & recovery
  - [ ] Implement snapshot mechanism
  - [ ] Create operation log
  - [ ] Build recovery system
- [ ] Networking & client interface
  - [ ] Socket-based server
  - [ ] Command-line client
  - [ ] Connection pooling

## 🤝 Contributing

This project is currently not accepting contributions as it's a personal learning exercise.

## 📄 License

All rights reserved. This project is not currently licensed for public use or distribution as it's a personal learning exercise.