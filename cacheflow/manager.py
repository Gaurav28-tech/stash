from dataclasses import dataclass
from typing import Any, Optional, Dict
import time
import threading
from cacheflow.lru import LRUCache
from cacheflow.lfu import LFUCache

@dataclass
class CacheStats:
    hits: int
    misses: int
    evictions: int
    hit_ratio: float
    total_keys: int

class CacheManager:
    def __init__(self, strategy: str = "lru", capacity: int = 128, default_ttl_seconds: Optional[float] = None):
        self.strategy = strategy.lower()
        self.capacity = capacity
        self.default_ttl = default_ttl_seconds
        self.backend = LRUCache(capacity) if self.strategy == "lru" else LFUCache(capacity)
        self.ttl_table: Dict[str, float] = {}
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            # Check TTL expiry
            if key in self.ttl_table:
                if time.time() > self.ttl_table[key]:
                    del self.ttl_table[key]
                    self.misses += 1
                    return None

            val = self.backend.get(key)
            if val is not None:
                self.hits += 1
                return val
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None):
        with self.lock:
            evicted = self.backend.set(key, value)
            if evicted:
                self.evictions += 1
                if evicted in self.ttl_table:
                    del self.ttl_table[evicted]

            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
            if ttl:
                self.ttl_table[key] = time.time() + ttl

    def get_stats(self) -> CacheStats:
        with self.lock:
            total = self.hits + self.misses
            ratio = (self.hits / total) if total > 0 else 0.0
            return CacheStats(
                hits=self.hits,
                misses=self.misses,
                evictions=self.evictions,
                hit_ratio=ratio,
                total_keys=len(self.backend)
            )
