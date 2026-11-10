from typing import Any, Optional, Dict
import threading

class _LRUNode:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['_LRUNode'] = None
        self.next: Optional['_LRUNode'] = None

class LRUCache:
    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.map: Dict[str, _LRUNode] = {}
        self.head = _LRUNode("", None)  # Dummy head (MRU)
        self.tail = _LRUNode("", None)  # Dummy tail (LRU)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = threading.Lock()

    def _remove(self, node: _LRUNode):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _LRUNode):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.map:
                return None
            node = self.map[key]
            self._remove(node)
            self._add_front(node)
            return node.value

    def set(self, key: str, value: Any) -> Optional[str]:
        with self.lock:
            evicted_key = None
            if key in self.map:
                node = self.map[key]
                node.value = value
                self._remove(node)
                self._add_front(node)
                return None

            if len(self.map) >= self.capacity:
                lru_node = self.tail.prev
                evicted_key = lru_node.key
                self._remove(lru_node)
                del self.map[evicted_key]

            new_node = _LRUNode(key, value)
            self.map[key] = new_node
            self._add_front(new_node)
            return evicted_key

    def __len__(self) -> int:
        with self.lock:
            return len(self.map)
