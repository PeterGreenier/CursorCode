"""
LeetCode 53. 最大子数组和
https://leetcode.com/problems/maximum-subarray/

给定整数数组 nums，找出具有最大和的连续子数组（至少包含一个元素），返回其和。
"""

from typing import List


def max_subarray(nums: List[int]) -> int:
    """
    Kadane 算法（动态规划）。

    思路：
    1. 维护 current_sum：以当前元素结尾的最大子数组和；
    2. 每步二选一——要么把当前元素接在前面的子数组后面，要么从当前元素重新开始；
    3. 用 max_sum 记录遍历过程中出现过的全局最大值。

    状态转移：current_sum = max(nums[i], current_sum + nums[i])
    """
    # 初始化为第一个元素，保证至少包含一个元素
    current_sum = max_sum = nums[0]

    for num in nums[1:]:
        # 接在前面的子数组后，或从当前元素重新开始
        current_sum = max(num, current_sum + num)
        # 更新全局最大和
        max_sum = max(max_sum, current_sum)

    return max_sum


class Solution:
    """LeetCode 提交格式。"""

    def maxSubArray(self, nums: List[int]) -> int:
        return max_subarray(nums)


if __name__ == "__main__":
    # 示例 1: 正负数混合，最优子数组 [4,-1,2,1]
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    # 示例 2: 单元素
    assert max_subarray([1]) == 1
    # 全正数
    assert max_subarray([5, 4, -1, 7, 8]) == 23
    # 全负数：取最大的单个元素
    assert max_subarray([-1, -2, -3]) == -1
    # 正负交替：最优子数组 [2,-1,2,3]
    assert max_subarray([2, -1, 2, 3, -4, 5]) == 7
    # 大负数夹在正数之间
    assert max_subarray([3, -10, 4, 5, -2, 6]) == 13
    # 前缀为负时应丢弃
    assert max_subarray([-5, 2, 3, -1, 4]) == 8
    print("All tests passed.")
