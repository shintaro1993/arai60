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
        num_paths[0][0] = 1
        for row in range(num_rows):
            for column in range(num_columns):
                if obstacleGrid[row][column] == OBSTACLE:
                    continue
                if row > 0:
                    num_paths[row][column] += num_paths[row - 1][column]
                if column > 0:
                    num_paths[row][column] += num_paths[row][column - 1]
        return num_paths[-1][-1]