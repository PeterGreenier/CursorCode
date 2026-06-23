"""
LeetCode 347. 前 K 个高频元素
https://leetcode.com/problems/top-k-frequent-elements/

给定整数数组 nums 和整数 k，返回出现频率前 k 高的元素，顺序不限。
"""

from collections import Counter
from typing import List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    桶排序解法。

    思路：
    1. 用哈希表统计每个元素的出现次数；
    2. 建立「频率桶」：下标 i 存放所有出现 i 次的元素；
    3. 从最高频率桶向低频率桶遍历，依次取出元素，直到凑满 k 个。

    为什么用桶排序而不是堆？
    - 堆解法时间 O(n log k)，桶排序在频率范围已知（1 ~ n）时为 O(n)。
    """
    # 统计每个元素的出现频率
    freq = Counter(nums)

    # buckets[i] 存放所有出现 i 次的元素；最多出现 len(nums) 次
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    # 从高频率向低频率收集结果
    result: List[int] = []
    for count in range(len(buckets) - 1, 0, -1):
        for num in buckets[count]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    """
    最小堆解法（备选实现）。

    维护大小为 k 的最小堆，堆顶是当前 Top-K 中频率最低的元素。
    当遇到更高频率的元素时，弹出堆顶并压入新元素。
    """
    import heapq

    freq = Counter(nums)
    # 堆元素：(频率, 数值)，堆顶为频率最小的
    heap: List[tuple[int, int]] = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]


class Solution:
    """LeetCode 提交格式。"""

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return top_k_frequent(nums, k)


if __name__ == "__main__":
    # 示例 1: [1,1,1,2,2,3], k=2 -> [1,2]
    assert set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    # 示例 2: [1], k=1 -> [1]
    assert set(top_k_frequent([1], 1)) == {1}
    # 堆解法结果一致
    assert set(top_k_frequent_heap([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    print("All tests passed.")
