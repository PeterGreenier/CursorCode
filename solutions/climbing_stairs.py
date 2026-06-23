"""
LeetCode 70. 爬楼梯
https://leetcode.com/problems/climbing-stairs/

每次可以爬 1 或 2 个台阶，求爬到第 n 阶楼梯的不同方法数。
"""

def climb_stairs(n: int) -> int:
    """
    动态规划。

    思路：
    1. 定义 dp[i] 为爬到第 i 阶的方法数；
    2. 最后一步要么从 i-1 阶爬 1 步，要么从 i-2 阶爬 2 步；
    3. 因此 dp[i] = dp[i - 1] + dp[i - 2]（斐波那契数列）。

    边界：dp[1] = 1，dp[2] = 2。
    """
    if n <= 2:
        return n

    # dp[i] 表示爬到第 i 阶的方法数
    dp = [0] * (n + 1)
    dp[1] = 1  # 只有 1 阶时，只有一种走法
    dp[2] = 2  # 2 阶：1+1 或 2

    for i in range(3, n + 1):
        # 从 i-1 爬 1 步 + 从 i-2 爬 2 步
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


class Solution:
    """LeetCode 提交格式。"""

    def climbStairs(self, n: int) -> int:
        return climb_stairs(n)


if __name__ == "__main__":
    # 示例 1: n = 2 → 1+1 或 2
    assert climb_stairs(2) == 2
    # 示例 2: n = 3 → 1+1+1, 1+2, 2+1
    assert climb_stairs(3) == 3
    # 边界: n = 1
    assert climb_stairs(1) == 1
    # n = 4 → 5 种
    assert climb_stairs(4) == 5
    # n = 5 → 8 种（斐波那契）
    assert climb_stairs(5) == 8
    # 较大输入
    assert climb_stairs(10) == 89
    print("All tests passed.")
