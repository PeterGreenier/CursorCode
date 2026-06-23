"""
LeetCode 88. 合并两个有序数组
https://leetcode.com/problems/merge-sorted-array/

将 nums2 合并进 nums1，使合并后的数组仍有序。
nums1 长度为 m + n，前 m 个为有效元素，后 n 个为空位。
"""

from typing import List


def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """
    原地合并：从尾部向前填充，避免覆盖 nums1 中尚未处理的元素。

    思路：
    1. 用三个指针 i、j、k，分别指向 nums1 有效末尾、nums2 末尾、合并后末尾；
    2. 每次取 i、j 处较大者写入 k，并左移对应指针；
    3. 若 nums2 仍有剩余，拷贝到 nums1 前部（nums1 剩余部分已在正确位置，无需处理）。
    """
    # i: nums1 中最后一个有效元素
    # j: nums2 中最后一个元素
    # k: 合并结果应写入的位置
    i, j, k = m - 1, n - 1, m + n - 1

    # 从后向前比较，将较大值放到 k 位置
    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    # nums2 若还有未合并元素，它们一定比 nums1 剩余部分更小，直接放到前面
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


class Solution:
    """LeetCode 提交格式。"""

    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        merge(nums1, m, nums2, n)


if __name__ == "__main__":
    # 示例 1: nums1 = [1,2,3,0,0,0], m=3, nums2 = [2,5,6], n=3
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

    # 示例 2: nums1 = [1], m=1, nums2 = [], n=0
    nums1 = [1]
    merge(nums1, 1, [], 0)
    assert nums1 == [1]

    # 示例 3: nums1 = [0], m=0, nums2 = [1], n=1
    nums1 = [0]
    merge(nums1, 0, [1], 1)
    assert nums1 == [1]

    # nums2 全部大于 nums1 有效部分
    nums1 = [2, 0, 0]
    merge(nums1, 1, [3, 4], 2)
    assert nums1 == [2, 3, 4]

    print("All tests passed.")
