from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        OBSTACLE = 1
        if not obstacleGrid:
            return 0
        if obstacleGrid[0][0] == OBSTACLE:
            return 0

        num_rows = len(obstacleGrid)
        num_columns = len(obstacleGrid[0])
        num_paths = [[0] * num_columns for _ in range(num_rows)]
        for row in range(num_rows):
            if obstacleGrid[row][0] == OBSTACLE:
                break
            num_paths[row][0] = 1
        for column in range(num_columns):
            if obstacleGrid[0][column] == OBSTACLE:
                break
            num_paths[0][column] = 1

        for row in range(1, num_rows):
            for column in range(1, num_columns):
                if obstacleGrid[row][column] == OBSTACLE:
                    continue
                num_paths[row][column] = (
                    num_paths[row - 1][column] + num_paths[row][column - 1]
                )
        return num_paths[-1][-1]


if __name__ == "__main__":
    s = Solution()
    assert s.uniquePathsWithObstacles([]) == 0
    assert s.uniquePathsWithObstacles([[1, 0], [0, 0]]) == 0
    assert s.uniquePathsWithObstacles([[0, 0], [0, 1]]) == 0
    assert s.uniquePathsWithObstacles([[1, 0], [0, 1]]) == 0
    assert s.uniquePathsWithObstacles([[0, 1, 0], [0, 0, 0], [0, 0, 0]]) == 3
    assert s.uniquePathsWithObstacles([[0, 1, 1], [0, 0, 0], [0, 0, 0]]) == 3
    assert s.uniquePathsWithObstacles([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) == 0
    assert s.uniquePathsWithObstacles([[0, 1, 0], [0, 1, 0], [0, 0, 0]]) == 1
    assert s.uniquePathsWithObstacles([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == 6
