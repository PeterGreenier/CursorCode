"""
LeetCode 200. 岛屿数量
https://leetcode.com/problems/number-of-islands/

给定由 '1'（陆地）和 '0'（水）组成的二维网格，计算岛屿数量。
岛屿被水包围，且通过水平或垂直方向相邻的陆地连接形成。
"""

from typing import List


def number_of_islands(grid: List[List[str]]) -> int:
    """
    DFS 遍历网格，统计连通块数量。

    思路：
    1. 遍历每个格子，遇到 '1' 时岛屿计数 +1；
    2. 从该格子出发 DFS，将与之四向连通的陆地全部标记为已访问（置为 '0'）；
    3. 重复直到遍历完整个网格。

    将访问过的陆地改为 '0'，避免额外 visited 数组，同时防止重复计数。
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        """从 (r, c) 出发，淹没整块陆地。"""
        # 越界或当前格不是陆地，停止扩展
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return

        # 标记已访问，防止重复进入
        grid[r][c] = "0"

        # 四向扩散：上、下、左、右
        dfs(r - 1, c)
        dfs(r + 1, c)
        dfs(r, c - 1)
        dfs(r, c + 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)

    return count


class Solution:
    """LeetCode 提交格式。"""

    def numIslands(self, grid: List[List[str]]) -> int:
        return number_of_islands(grid)


if __name__ == "__main__":
    # 示例 1:
    # 11110    岛屿 1
    # 11010    岛屿 2
    # 11000
    # 00000
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert number_of_islands([row[:] for row in grid1]) == 1

    # 示例 2:
    # 11000    岛屿 1
    # 11000    岛屿 2
    # 00100    岛屿 3
    # 00011
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert number_of_islands([row[:] for row in grid2]) == 3

    # 边界: 空网格
    assert number_of_islands([]) == 0
    # 边界: 全水
    assert number_of_islands([["0", "0"], ["0", "0"]]) == 0
    # 边界: 全陆（一块岛屿）
    assert number_of_islands([["1", "1"], ["1", "1"]]) == 1
    # 边界: 单行
    assert number_of_islands([["1", "0", "1"]]) == 2

    print("All tests passed.")
