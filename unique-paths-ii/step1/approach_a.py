from typing import List


OBSTACLE = 1


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if not obstacleGrid:
            return 0
        if obstacleGrid[0][0] == OBSTACLE:
            return 0
        if obstacleGrid[-1][-1] == OBSTACLE:
            return 0

        num_rows = len(obstacleGrid)
        num_columns = len(obstacleGrid[0])
        num_paths = [[0] * num_columns for _ in range(num_rows)]
        num_paths[0][0] = 1
        for row in range(1, num_rows):
            if obstacleGrid[row - 1][0] == OBSTACLE:
                continue
            num_paths[row][0] = num_paths[row - 1][0]
        for column in range(1, num_columns):
            if obstacleGrid[0][column - 1] == OBSTACLE:
                continue
            num_paths[0][column] = num_paths[0][column - 1]

        for row in range(1, num_rows):
            for column in range(1, num_columns):
                if obstacleGrid[row - 1][column] != OBSTACLE:
                    num_paths[row][column] += num_paths[row - 1][column]
                if obstacleGrid[row][column - 1] != OBSTACLE:
                    num_paths[row][column] += num_paths[row][column - 1]
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
