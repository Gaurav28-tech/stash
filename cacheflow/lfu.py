from collections import defaultdict, OrderedDict
from typing import Any, Optional, Dict
import threading

class LFUCache:
    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.vals: Dict[str, Any] = {}
        self.counts: Dict[str, int] = {}
        self.freq_buckets: Dict[int, OrderedDict] = defaultdict(OrderedDict)
        self.min_freq = 0
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.vals:
                return None
            count = self.counts[key]
            self.counts[key] = count + 1
            del self.freq_buckets[count][key]

            if not self.freq_buckets[count] and self.min_freq == count:
                self.min_freq += 1

            self.freq_buckets[count + 1][key] = None
            return self.vals[key]

    def set(self, key: str, value: Any) -> Optional[str]:
        with self.lock:
            if key in self.vals:
                self.vals[key] = value
                self.get(key)
                return None

            evicted_key = None
            if len(self.vals) >= self.capacity:
                evicted_key, _ = self.freq_buckets[self.min_freq].popitem(last=False)
                del self.vals[evicted_key]
                del self.counts[evicted_key]

            self.vals[key] = value
            self.counts[key] = 1
            self.freq_buckets[1][key] = None
            self.min_freq = 1
            return evicted_key

    def __len__(self) -> int:
        with self.lock:
            return len(self.vals)
