"""
LeetCode 322. 零钱兑换
https://leetcode.com/problems/coin-change/

给定不同面额的硬币 coins 和一个总金额 amount，
计算可以凑成总金额所需的最少硬币个数。
若无法凑成，返回 -1。
"""

from typing import List


def coin_change(coins: List[int], amount: int) -> int:
    """
    动态规划（完全背包，求最小值）。

    思路：
    1. 定义 dp[i] 为凑成金额 i 所需的最少硬币数；
    2. 对每个金额 i，尝试使用每一种硬币 coin：
       若 coin <= i，则 dp[i] = min(dp[i], dp[i - coin] + 1)；
    3. 初始时 dp[0] = 0（凑 0 元不需要硬币），其余为无穷大。

    边界：amount == 0 时返回 0；无法凑成时返回 -1。
    """
    if amount == 0:
        return 0

    # dp[i] 表示凑成金额 i 所需的最少硬币数
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0  # 凑 0 元不需要任何硬币

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                # 使用一枚 coin 后，剩余 i - coin 的最优解 + 1
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


class Solution:
    """LeetCode 提交格式。"""

    def coinChange(self, coins: List[int], amount: int) -> int:
        return coin_change(coins, amount)


if __name__ == "__main__":
    # 示例 1: coins = [1,2,5], amount = 11 → 5+5+1 = 3 枚
    assert coin_change([1, 2, 5], 11) == 3
    # 示例 2: coins = [2], amount = 3 → 无法凑成
    assert coin_change([2], 3) == -1
    # 示例 3: coins = [1], amount = 0 → 0 枚
    assert coin_change([1], 0) == 0
    # 单枚硬币刚好凑齐
    assert coin_change([1, 2, 5], 5) == 1
    # 大面额优先
    assert coin_change([1, 3, 4], 6) == 2  # 3+3
    # 无解：硬币面额均大于目标
    assert coin_change([5, 10], 3) == -1
    print("All tests passed.")
