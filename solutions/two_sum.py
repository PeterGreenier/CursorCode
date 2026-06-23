"""
LeetCode 1. 两数之和
https://leetcode.com/problems/two-sum/

给定整数数组 nums 和目标值 target，返回和为 target 的两个数的下标。
假设每种输入恰好对应一个答案，且同一元素不可重复使用。
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    """
    哈希表一次遍历。

    思路：
    1. 遍历数组，对每个元素 nums[i]，计算补数 complement = target - nums[i]；
    2. 若 complement 已在哈希表中，说明之前见过配对元素，返回两个下标；
    3. 否则将当前值及其下标存入哈希表，供后续元素查找。

    为什么只需一次遍历：若存在 nums[i] + nums[j] = target（i < j），
    当遍历到 j 时，nums[i] 已作为 complement 存入表中，可立即命中。
    """
    # 值 -> 下标，用于 O(1) 查找补数
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            # 先见到的下标在前，保证返回顺序与题目示例一致
            return [seen[complement], i]

        # 当前数尚未配对，记录其下标
        seen[num] = i

    # 题目保证有解，正常不会执行到这里
    return []


class Solution:
    """LeetCode 提交格式。"""

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        return two_sum(nums, target)


if __name__ == "__main__":
    # 示例 1: [2,7,11,15], target=9 -> [0,1]
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    # 示例 2: [3,2,4], target=6 -> [1,2]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    # 示例 3: [3,3], target=6 -> [0,1]
    assert two_sum([3, 3], 6) == [0, 1]

    # 边界: 两元素数组
    assert two_sum([1, 2], 3) == [0, 1]
    # 边界: 含负数
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
    # 边界: 正负混合
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]

    print("All tests passed.")
