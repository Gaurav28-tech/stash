import os
import sys
import unittest
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cacheflow.lru import LRUCache
from cacheflow.lfu import LFUCache
from cacheflow.manager import CacheManager

class TestCacheFlow(unittest.TestCase):
    def test_lru_eviction(self):
        cache = LRUCache(capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertEqual(cache.get("a"), 1)  # accessed "a", so "b" is now LRU
        
        cache.set("c", 3)  # should evict "b"
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_lfu_eviction(self):
        cache = LFUCache(capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.get("a")  # freq(a)=2, freq(b)=1

        cache.set("c", 3)  # should evict "b" (freq 1)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_cache_manager_ttl_and_stats(self):
        mgr = CacheManager(strategy="lru", capacity=10, default_ttl_seconds=0.1)
        mgr.set("key1", "val1")
        self.assertEqual(mgr.get("key1"), "val1")

        time.sleep(0.15)
        self.assertIsNone(mgr.get("key1"))

        stats = mgr.get_stats()
        self.assertEqual(stats.hits, 1)
        self.assertEqual(stats.misses, 1)
        self.assertEqual(stats.hit_ratio, 0.5)

if __name__ == "__main__":
    unittest.main()
