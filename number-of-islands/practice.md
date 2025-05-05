# Step1 のコードの書き換え

## Step1

- next_lands を list から deque に変えて、幅優先探索のように探索を行う
- deque の初期化方法に注意
    - https://docs.python.org/3/library/collections.html#collections.deque

```python

class Solution:
    def is_valid_next(self, grid, seen_lands, next_row, next_col):
        if next_row < 0 or len(grid) <= next_row or next_col < 0 or len(grid[0]) <= next_col:
            return False
        if grid[next_row][next_col] == "0" or (next_row, next_col) in seen_lands:
            return False
        return True

    def traverse_island(self, grid, seen_lands, start_row, start_col):
        next_lands = deque([(start_row, start_col)])
        seen_lands.add((start_row, start_col))

        while next_lands:
            row, col = next_lands.popleft()
            for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row = row + d_row
                next_col = col + d_col
                if self.is_valid_next(grid, seen_lands,next_row, next_col):
                    next_lands.append((next_row, next_col))
                    seen_lands.add((next_row, next_col))

    def numIslands(self, grid: List[List[str]]) -> int:
        result = 0
        seen_lands = set()

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "0" or (row, col) in seen_lands:
                    continue
                self.traverse_island(grid, seen_lands, row, col)
                result += 1

        return result

```

- next_lands で list を使っているコードを、再帰を使って実装したものです。

```python

class Solution:
    def is_valid_next(self, grid, seen_lands, row, col):
        if row < 0 or len(grid) <= row or col < 0 or len(grid[0]) <= col:
            return False
        if grid[row][col] == "0" or (row, col) in seen_lands:
            return False
        return True

    def traverse_island(self, grid, seen_lands, row, col):
        for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_row = row + d_row
            next_col = col + d_col
            if self.is_valid_next(grid, seen_lands,next_row, next_col):
                seen_lands.add((next_row, next_col))
                self.traverse_island(grid, seen_lands, next_row, next_col)

    def numIslands(self, grid: List[List[str]]) -> int:
        result = 0
        seen_lands = set()

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "0" or (row, col) in seen_lands:
                    continue
                seen_lands.add((row, col))
                self.traverse_island(grid, seen_lands, row, col)
                result += 1

        return result

```

## Step2

- 復習のときに step2 もやる