class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        if m <= 0 or n <= 0:
            return 0

        num_paths = [[0] * n for _ in range(m)]
        for row in range(m):
            num_paths[row][0] = 1
        for column in range(n):
            num_paths[0][column] = 1

        for row in range(1, m):
            for column in range(1, n):
                num_paths[row][column] = (
                    num_paths[row - 1][column] + num_paths[row][column - 1]
                )
        return num_paths[-1][-1]


if __name__ == "__main__":
    s = Solution()
    assert s.uniquePaths(0, 0) == 0
    assert s.uniquePaths(1, 0) == 0
    assert s.uniquePaths(0, 1) == 0
    assert s.uniquePaths(1, 1) == 1
    assert s.uniquePaths(1, 2) == 1
    assert s.uniquePaths(2, 2) == 2
    assert s.uniquePaths(2, 3) == 3
