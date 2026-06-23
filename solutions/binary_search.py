"""
LeetCode 704. 二分查找
https://leetcode.com/problems/binary-search/

在有序数组 nums 中查找 target，返回下标；不存在则返回 -1。
"""

from typing import List


def binary_search(nums: List[int], target: int) -> int:
    """
    经典二分查找。

    思路：
    1. 维护搜索区间 [left, right]（闭区间）；
    2. 每次取中点 mid，与 target 比较；
    3. 相等则返回 mid；target 更小则收缩右边界，更大则收缩左边界；
    4. 区间为空时说明不存在，返回 -1。
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        # 使用 left + (right - left) // 2 避免 (left + right) 整数溢出
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            # target 在右半部分，排除 mid 及左侧
            left = mid + 1
        else:
            # target 在左半部分，排除 mid 及右侧
            right = mid - 1

    return -1


class Solution:
    """LeetCode 提交格式。"""

    def search(self, nums: List[int], target: int) -> int:
        return binary_search(nums, target)


if __name__ == "__main__":
    # 示例 1: target 存在
    assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
    # 示例 2: target 不存在
    assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1

    # 边界: 空数组
    assert binary_search([], 5) == -1
    # 边界: 单元素，命中
    assert binary_search([7], 7) == 0
    # 边界: 单元素，未命中
    assert binary_search([7], 3) == -1

    # 边界: target 在首元素
    assert binary_search([1, 2, 3, 4, 5], 1) == 0
    # 边界: target 在末元素
    assert binary_search([1, 2, 3, 4, 5], 5) == 4
    # 边界: target 小于最小值
    assert binary_search([1, 2, 3, 4, 5], 0) == -1
    # 边界: target 大于最大值
    assert binary_search([1, 2, 3, 4, 5], 6) == -1

    # 边界: 两个元素
    assert binary_search([1, 3], 1) == 0
    assert binary_search([1, 3], 3) == 1
    assert binary_search([1, 3], 2) == -1

    print("All tests passed.")
