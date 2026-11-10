# CacheFlow ⚡

[![CI](https://github.com/Gaurav28-tech/cache-flow/actions/workflows/ci.yml/badge.svg)](https://github.com/Gaurav28-tech/cache-flow)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)]()

**CacheFlow** is a concurrent, high-performance in-memory caching engine engineered in Python. It supports pluggable eviction algorithms—including Least Recently Used (**LRU**), Least Frequently Used (**LFU**), and Millisecond Time-to-Live (**TTL**)—alongside comprehensive cache efficiency telemetry.

---

## 🚀 Key Features

- **O(1) LRU Cache**: Implemented with doubly-linked lists and hash maps for constant-time lookups and evictions.
- **O(1) LFU Cache**: Frequency bucket architecture maintaining strict O(1) performance during frequency increments and evictions.
- **Precision TTL**: Lazy and active expiration sweeps for millisecond time-sensitive data.
- **Cache Observability**: Real-time telemetry tracking hit/miss ratios, eviction counts, and memory footprint estimations.
- **Thread-Safe**: Synchronized primitives ensuring concurrent thread safety across high-throughput web servers.

---

## 🏗️ Architecture

```
                  +--------------------------+
                  |    CacheFlow Manager     |
                  +--------------------------+
                               |
            +------------------+------------------+
            |                  |                  |
            v                  v                  v
     [LRU Strategy]     [LFU Strategy]     [TTL Strategy]
   (Doubly-Linked List)(Frequency Buckets) (Timestamp Ring)
            |                  |                  |
            +------------------+------------------+
                               |
                               v
                     [Telemetry Collector]
                     (Hits, Misses, Ratios)
```

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Gaurav28-tech/cache-flow.git
cd cache-flow
```

### Basic Usage

```python
from cacheflow.lru import LRUCache
from cacheflow.lfu import LFUCache
from cacheflow.manager import CacheManager

# 1. Use the unified Cache Manager
cache = CacheManager(strategy="lru", capacity=100, default_ttl_seconds=60.0)

cache.set("user:101", {"name": "Alice", "role": "admin"})
user = cache.get("user:101")
print(f"Retrieved: {user}")

# Check Telemetry Metrics
stats = cache.get_stats()
print(f"Hit Ratio: {stats.hit_ratio:.2%}, Evictions: {stats.evictions}")
```

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
