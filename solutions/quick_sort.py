"""
快速排序（原地 partition + 递归）

对数组进行原地升序排序。
"""

import random
from typing import List


def partition(arr: List[int], low: int, high: int) -> int:
    """
    原地分区：以 arr[high] 为枢轴，将区间 [low, high] 划分为
    「小于等于枢轴」与「大于枢轴」两部分，返回枢轴最终下标。

    使用 Lomuto 分区方案：
    - i 指向「小于等于枢轴」区域的最后一个位置；
    - j 从左向右扫描，遇到 <= pivot 的元素则与 i+1 交换并扩展左区。
    """
    pivot = arr[high]
    # i 左侧（含 i）均为 <= pivot 的元素
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # 将枢轴放到正确位置：左区 | pivot | 右区
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr: List[int], low: int, high: int) -> None:
    """
    递归快速排序：对 arr[low:high] 原地升序排列。

    1. 若 low >= high，区间长度 <= 1，无需处理；
    2. partition 得到枢轴位置 p；
    3. 分别对 [low, p-1] 与 [p+1, high] 递归排序。
    """
    if low >= high:
        return

    pivot_index = partition(arr, low, high)
    quick_sort(arr, low, pivot_index - 1)
    quick_sort(arr, pivot_index + 1, high)


def quick_sort_inplace(arr: List[int]) -> None:
    """对整段数组原地快速排序的便捷入口。"""
    if not arr:
        return
    quick_sort(arr, 0, len(arr) - 1)


def is_sorted(arr: List[int]) -> bool:
    """检查数组是否非降序。"""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


if __name__ == "__main__":
    # 固定用例
    sample = [3, 6, 8, 10, 1, 2, 1]
    quick_sort_inplace(sample)
    assert sample == [1, 1, 2, 3, 6, 8, 10]

    # 边界：空数组、单元素
    empty: List[int] = []
    quick_sort_inplace(empty)
    assert empty == []

    single = [42]
    quick_sort_inplace(single)
    assert single == [42]

    # 边界：已有序、逆序、全相同
    sorted_arr = [1, 2, 3, 4, 5]
    quick_sort_inplace(sorted_arr)
    assert sorted_arr == [1, 2, 3, 4, 5]

    reversed_arr = [5, 4, 3, 2, 1]
    quick_sort_inplace(reversed_arr)
    assert reversed_arr == [1, 2, 3, 4, 5]

    duplicates = [2, 2, 2, 2]
    quick_sort_inplace(duplicates)
    assert duplicates == [2, 2, 2, 2]

    # 随机数组测试：多次生成并验证有序
    random.seed(2026)
    for size in (0, 1, 2, 10, 100, 500):
        for _ in range(20):
            original = [random.randint(-1000, 1000) for _ in range(size)]
            expected = sorted(original)
            arr = original.copy()
            quick_sort_inplace(arr)
            assert arr == expected, f"size={size}, original={original}, got={arr}"
            assert is_sorted(arr)

    print("All tests passed.")
