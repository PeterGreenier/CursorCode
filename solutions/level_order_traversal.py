"""
LeetCode 102. 二叉树的层序遍历
https://leetcode.com/problems/binary-tree-level-order-traversal/

给定二叉树根节点，返回节点值的层序遍历结果（逐层从左到右）。
"""

from collections import deque
from typing import Deque, List, Optional


class TreeNode:
    """二叉树节点。"""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    BFS 层序遍历。

    思路：
    1. 用队列存放待访问节点，初始放入根节点；
    2. 每次取出当前层的全部节点（队列长度即为层大小），
       依次访问并把它们的孩子入队；
    3. 重复直到队列为空。

    关键：在每一轮循环开始时记录 queue 的长度，
    只处理这一批节点，即可自然按层分组。
    """
    if root is None:
        return []

    result: List[List[int]] = []
    queue: Deque[TreeNode] = deque([root])

    while queue:
        level_size = len(queue)
        current_level: List[int] = []

        # 处理当前层的 level_size 个节点
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        result.append(current_level)

    return result


class Solution:
    """LeetCode 提交格式。"""

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        return level_order(root)


if __name__ == "__main__":
    # 示例 1: [3,9,20,null,null,15,7] -> [[3],[9,20],[15,7]]
    root1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert level_order(root1) == [[3], [9, 20], [15, 7]]

    # 示例 2: [1] -> [[1]]
    root2 = TreeNode(1)
    assert level_order(root2) == [[1]]

    # 空树 -> []
    assert level_order(None) == []

    print("All tests passed.")
