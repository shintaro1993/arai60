class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        if m <= 0 or n <= 0:
            return 0

        path_counts = [[0] * n for _ in range(m)]
        for row in range(m):
            path_counts[row][0] = 1
        for col in range(n):
            path_counts[0][col] = 1

        for row in range(1, m):
            for col in range(1, n):
                path_counts[row][col] = (
                    path_counts[row - 1][col] + path_counts[row][col - 1]
                )
        return path_counts[m - 1][n - 1]


if __name__ == "__main__":
    s = Solution()
    assert s.uniquePaths(0, 0) == 0
    assert s.uniquePaths(1, 0) == 0
    assert s.uniquePaths(0, 1) == 0
    assert s.uniquePaths(1, 1) == 1
    assert s.uniquePaths(1, 2) == 1
    assert s.uniquePaths(2, 2) == 2
    assert s.uniquePaths(2, 3) == 3
