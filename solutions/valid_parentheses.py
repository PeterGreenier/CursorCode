"""
LeetCode 20. 有效的括号
https://leetcode.com/problems/valid-parentheses/

给定只包含 '(', ')', '{', '}', '[', ']' 的字符串 s，判断括号是否有效。
"""


def is_valid(s: str) -> bool:
    """
    栈匹配括号。

    思路：
    1. 遇到左括号时入栈，等待后续右括号配对；
    2. 遇到右括号时，栈顶必须是与之对应的左括号，否则无效；
    3. 遍历结束后栈应为空，否则有未闭合的左括号。

    时间复杂度 O(n)，空间复杂度 O(n)。
    """
    # 右括号 → 左括号的映射，用于快速判断配对
    pairs = {")": "(", "}": "{", "]": "["}
    stack: list[str] = []

    for ch in s:
        if ch in pairs:
            # 右括号：栈空或栈顶不匹配则无效
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            # 左括号：先入栈等待配对
            stack.append(ch)

    # 栈空说明所有括号均已正确闭合
    return not stack


class Solution:
    """LeetCode 提交格式。"""

    def isValid(self, s: str) -> bool:
        return is_valid(s)


if __name__ == "__main__":
    # 示例 1: 简单嵌套
    assert is_valid("()") is True
    # 示例 2: 多种括号嵌套
    assert is_valid("()[]{}") is True
    # 示例 3: 顺序错误
    assert is_valid("(]") is False
    # 示例 4: 未闭合的左括号
    assert is_valid("((") is False
    # 示例 5: 多余的右括号
    assert is_valid("())") is False
    # 嵌套多层
    assert is_valid("{[]}") is True
    # 交错错误
    assert is_valid("([)]") is False
    # 空字符串（LeetCode 约束下通常非空，但逻辑上有效）
    assert is_valid("") is True
    # 单对花括号
    assert is_valid("{}") is True
    print("All tests passed.")
