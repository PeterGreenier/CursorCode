"""
LeetCode 3. 无重复字符的最长子串
https://leetcode.com/problems/longest-substring-without-repeating-characters/

给定字符串 s，找出不含重复字符的最长子串的长度。
"""

from typing import Dict


def length_of_longest_substring(s: str) -> int:
    """
    滑动窗口 + 哈希表记录字符最近出现位置。

    思路：
    1. 用 [left, right] 维护当前无重复子串的窗口；
    2. 右指针逐字符扩展窗口，哈希表记录每个字符最近一次的下标；
    3. 若当前字符在窗口内已出现过，将左指针跳到该字符上次位置的下一位；
    4. 每步更新窗口长度，取全局最大值。
    """
    # 字符 -> 最近一次出现的下标
    last_seen: Dict[str, int] = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # 重复字符落在当前窗口内时，收缩左边界
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        # 记录当前字符位置，并更新最长长度
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


class Solution:
    """LeetCode 提交格式。"""

    def lengthOfLongestSubstring(self, s: str) -> int:
        return length_of_longest_substring(s)


if __name__ == "__main__":
    # 示例 1: "abcabcbb" -> 3 ("abc")
    assert length_of_longest_substring("abcabcbb") == 3
    # 示例 2: "bbbbb" -> 1 ("b")
    assert length_of_longest_substring("bbbbb") == 1
    # 示例 3: "pwwkew" -> 3 ("wke")
    assert length_of_longest_substring("pwwkew") == 3
    # 空字符串
    assert length_of_longest_substring("") == 0
    # 单字符
    assert length_of_longest_substring("a") == 1
    # 无重复
    assert length_of_longest_substring("abcdef") == 6
    # 重复字符在窗口外，左边界不必移动
    assert length_of_longest_substring("abba") == 2
    # 含空格
    assert length_of_longest_substring("a b c a") == 3
    print("All tests passed.")
