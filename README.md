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

- ✅ Hash Table implementation (core data structure)
- ✅ Unit tests for Hash Table

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

## 📝 Usage (Coming Soon)

```python
# Sample usage will be available once the core database is implemented
from pycachedb.core import PyCacheDB

db = PyCacheDB()
db.execute("SET user:1 'John Doe'")
user = db.execute("GET user:1")
```

## 🏗️ Project Structure

```
pycachedb/
│
├── data_structures/         # Core data structures
│   ├── __init__.py
│   └── hash_table.py        # Hash table implementation
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_hash_table.py   # Tests for hash table
│
├── run_tests.bat            # Test runner for Windows
└── README.md                # This file
```

## 📋 Implementation Plan

### Core Data Structures (Completed)
- [x] Hash table for key-value storage

### Next Steps
- [ ] Linked list for LRU functionality
- [ ] Query language parser
- [ ] Data types & operations
- [ ] Cache eviction policies
- [ ] Persistence & recovery
- [ ] Networking & client interface

## 🤝 Contributing

This project is currently not accepting contributions as it's a personal learning exercise.

## 📄 License

All rights reserved. This project is not currently licensed for public use or distribution as it's a personal learning exercise.