"""
LeetCode 146. LRU 缓存
https://leetcode.com/problems/lru-cache/

实现 LRU（最近最少使用）缓存，支持 get 和 put，均要求 O(1) 时间复杂度。

OrderedDict 内部维护双向链表 + 哈希表：
- 哈希表提供 O(1) 按键查找
- 双向链表维护访问顺序（头部最久未用，尾部最近使用）
"""

from collections import OrderedDict


class LRUCache:
    """
    LRU 缓存，容量满时淘汰最久未访问的键。

    使用 OrderedDict 简化双向链表操作：
    - move_to_end(key)  将键移到尾部，标记为「最近使用」
    - popitem(last=False) 弹出头部，即淘汰 LRU 项
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        # 键 -> 值；插入顺序即 LRU 顺序（左侧最旧，右侧最新）
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        """获取键对应的值；不存在时返回 -1，并将该键标记为最近使用。"""
        if key not in self.cache:
            return -1

        # 访问后移到尾部，表示「刚被使用过」
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """写入或更新键值；超出容量时淘汰最久未使用的键。"""
        if key in self.cache:
            # 已存在的键：先移到尾部，再更新值
            self.cache.move_to_end(key)

        self.cache[key] = value

        # 超出容量，弹出头部（最久未使用）
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class Solution:
    """LeetCode 提交格式（类名需为 LRUCache，此处仅作项目内统一结构）。"""

    def create(self, capacity: int) -> LRUCache:
        return LRUCache(capacity)


if __name__ == "__main__":
    # 示例 1: capacity=2
    # ["LRUCache","put","put","get","put","get","put","get","get","get"]
    # [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
    cache = LRUCache(2)
    cache.put(1, 1)  # 缓存 {1=1}
    cache.put(2, 2)  # 缓存 {1=1, 2=2}
    assert cache.get(1) == 1     # 返回 1，缓存 {2=2, 1=1}
    cache.put(3, 3)              # 淘汰 key 2，缓存 {1=1, 3=3}
    assert cache.get(2) == -1   # key 2 已被淘汰
    cache.put(4, 4)              # 淘汰 key 1，缓存 {3=3, 4=4}
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

    # 边界: 容量为 1
    cache1 = LRUCache(1)
    cache1.put(1, 10)
    assert cache1.get(1) == 10
    cache1.put(2, 20)  # 淘汰 key 1
    assert cache1.get(1) == -1
    assert cache1.get(2) == 20

    # 边界: 更新已存在的键（不应增加条目数，但应标记为最近使用）
    cache2 = LRUCache(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    cache2.put(1, 10)  # 更新 key 1，key 1 变为最近使用
    cache2.put(3, 3)   # 应淘汰 key 2 而非 key 1
    assert cache2.get(2) == -1
    assert cache2.get(1) == 10
    assert cache2.get(3) == 3

    # 边界: 连续 get 同一键
    cache3 = LRUCache(2)
    cache3.put(1, 1)
    cache3.put(2, 2)
    assert cache3.get(1) == 1
    assert cache3.get(1) == 1  # 多次访问不影响正确性
    cache3.put(3, 3)           # key 2 最久未用，应被淘汰
    assert cache3.get(2) == -1

    print("All tests passed.")
