"""
LeetCode 234. 回文链表
https://leetcode.com/problems/palindrome-linked-list/

给定单链表的头节点 head，判断该链表是否为回文链表。
要求 O(n) 时间、O(1) 额外空间。
"""

from typing import List, Optional


class ListNode:
    """单链表节点。"""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """迭代反转链表，返回新头节点。"""
    prev: Optional[ListNode] = None
    curr = head

    while curr is not None:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    return prev


def is_palindrome(head: Optional[ListNode]) -> bool:
    """
    快慢指针找中点 + 反转后半段 + 逐节点比较。

    思路：
    1. 快指针每次走 2 步、慢指针走 1 步，快指针到末尾时慢指针在中点；
    2. 反转慢指针之后的后半段链表；
    3. 从头节点与反转后的后半段头同时遍历，比较每个节点的值；
    4. 比较结束后将后半段再反转回来，恢复链表原貌（不影响判题，但便于调试）。

    示例：1 -> 2 -> 2 -> 1
    中点后半段 2 -> 1，反转得 1 -> 2，与前半段 1 -> 2 一一对应。
    """
    if head is None or head.next is None:
        return True

    # 第一步：快慢指针定位后半段起点
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next

    # slow 此时位于前半段最后一个节点（偶数长度）或中点偏左（奇数长度）
    second_half_head = reverse_list(slow.next)
    slow.next = None  # 断开前后两半，便于比较与后续恢复

    # 第二步：逐节点比较前半段与反转后的后半段
    left = head
    right = second_half_head
    is_pal = True

    while right is not None:
        if left.val != right.val:
            is_pal = False
            break
        left = left.next
        right = right.next

    # 第三步：恢复链表结构
    slow.next = reverse_list(second_half_head)

    return is_pal


def build_list(values: List[int]) -> Optional[ListNode]:
    """由数组构建链表，便于测试。"""
    if not values:
        return None

    dummy = ListNode()
    tail = dummy
    for val in values:
        tail.next = ListNode(val)
        tail = tail.next
    return dummy.next


class Solution:
    """LeetCode 提交格式。"""

    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        return is_palindrome(head)


if __name__ == "__main__":
    # 示例 1: [1,2,2,1] -> True
    assert is_palindrome(build_list([1, 2, 2, 1])) is True

    # 示例 2: [1,2] -> False
    assert is_palindrome(build_list([1, 2])) is False

    # 边界: 空链表
    assert is_palindrome(None) is True

    # 边界: 单节点
    assert is_palindrome(build_list([1])) is True

    # 边界: 奇数长度回文
    assert is_palindrome(build_list([1, 2, 3, 2, 1])) is True

    # 边界: 奇数长度非回文
    assert is_palindrome(build_list([1, 2, 3, 4, 5])) is False

    # 边界: 偶数长度非回文
    assert is_palindrome(build_list([1, 2, 3, 4])) is False

    print("All tests passed.")
