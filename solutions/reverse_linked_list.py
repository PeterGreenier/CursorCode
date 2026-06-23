"""
LeetCode 206. 反转链表
https://leetcode.com/problems/reverse-linked-list/

给定单链表的头节点 head，反转链表并返回反转后的头节点。
"""

from typing import List, Optional


class ListNode:
    """单链表节点。"""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    迭代法反转单链表。

    思路：
    1. 维护三个指针：prev（已反转部分的头）、curr（当前待处理节点）、next_node（暂存后继）；
    2. 每次将 curr.next 指向 prev，完成当前节点的反转；
    3. 三个指针同步前移，直到 curr 为 None；
    4. 返回 prev，即新链表头。

    示例：1 -> 2 -> 3 -> None
    步骤后变为 None <- 1 <- 2 <- 3，prev 指向 3。
    """
    prev: Optional[ListNode] = None
    curr = head

    while curr is not None:
        # 先保存后继，避免断链后丢失剩余部分
        next_node = curr.next
        # 反转当前节点的指向
        curr.next = prev
        # 前移：prev 和 curr 各进一步
        prev = curr
        curr = next_node

    return prev


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


def list_to_array(head: Optional[ListNode]) -> List[int]:
    """将链表转为数组，便于断言。"""
    result: List[int] = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


class Solution:
    """LeetCode 提交格式。"""

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return reverse_list(head)


if __name__ == "__main__":
    # 示例 1: [1,2,3,4,5] -> [5,4,3,2,1]
    head1 = build_list([1, 2, 3, 4, 5])
    assert list_to_array(reverse_list(head1)) == [5, 4, 3, 2, 1]

    # 示例 2: [1,2] -> [2,1]
    head2 = build_list([1, 2])
    assert list_to_array(reverse_list(head2)) == [2, 1]

    # 示例 3: 空链表 -> []
    assert reverse_list(None) is None
    assert list_to_array(reverse_list(None)) == []

    # 边界: 单节点
    head3 = build_list([1])
    assert list_to_array(reverse_list(head3)) == [1]

    # 边界: 含重复值
    head4 = build_list([1, 1, 2, 2])
    assert list_to_array(reverse_list(head4)) == [2, 2, 1, 1]

    print("All tests passed.")
