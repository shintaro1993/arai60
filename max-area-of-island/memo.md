# 695. Max Area of Island

## Step1

- 考えたこと
    - island の探索をするときに island の大きさも数えるとよさそう。
    - ある land を二回以上スタックに積まないことを保証しておいて、スタックに積むときか取り出すときに island の数を増やしていく。
    - 受け取ったリストを破壊することは期待されてなさそうだと思います。
    - 発見済みノードの管理方法は set の他にリストを自分で作るか、受け取った grid をコピーするかとかかな。set を使って `(row, col) in seen` と書けるほうが自分は好きかな。

- 見積り
    - n: len(grid)
    - m: len(grid[0])
    - 時間計算量: O(n * m)
    - 空間計算量: O(n * m)

```python

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        WATER = 0
        num_rows = len(grid)
        num_cols = len(grid[0])
        seen = set()

        def inside_grid(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols

        def can_visit(row, col):
            return not(grid[row][col] == WATER or (row, col) in seen)

        def measure_island_area(start_row, start_col):
            next_lands = [(start_row, start_col)]
            seen.add((start_row, start_col))
            result = 0
            
            while next_lands:
                row, col = next_lands.pop()
                result += 1
                for delta_row, delta_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_row = row + delta_row
                    next_col = col + delta_col
                    if not inside_grid(next_row, next_col):
                        continue
                    if not can_visit(next_row, next_col):
                        continue
                    next_lands.append((next_row, next_col))
                    seen.add((next_row, next_col))

            return result

        max_area = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if not can_visit(row, col):
                    continue
                max_area = max(max_area, measure_island_area(row, col))

        return max_area

```

- 見つけた land をとりあえずスタックに積んで、取り出すときに数えても大丈夫か確認するということもできそう。

```python

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        WATER = 0
        num_rows = len(grid)
        num_cols = len(grid[0])
        visited = set()

        def inside_grid(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols

        def can_visit(row, col):
            return not(grid[row][col] == WATER or (row, col) in visited)

        def measure_island_area(start_row, start_col):
            next_lands = [(start_row, start_col)]
            result = 0
            
            while next_lands:
                row, col = next_lands.pop()
                if not inside_grid(row, col):
                    continue
                if not can_visit(row, col):
                    continue
                visited.add((row, col))
                result += 1
                next_lands.append((row + 1, col))
                next_lands.append((row - 1, col))
                next_lands.append((row, col + 1))
                next_lands.append((row, col - 1))
                        
            return result

        max_area = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if not can_visit(row, col):
                    continue
                max_area = max(max_area, measure_island_area(row, col))

        return max_area

```

## Step2

### 調べたこと・読んだコード

- https://github.com/YukiMichishita/LeetCode/pull/6/files
    - 自分は height, width より num_rows, num_cols の方が好きそう。
    - a[y][x] は、y が縦に移動していると考えると自然になるのかな。
    - unionfind も見ておこう。
- https://github.com/colorbox/leetcode/pull/32/files
    - Step1 のコード、片方の関数で定義した `row_count = grid.size()` をもう片方の関数で使わず `grid.size()` を使っている。自分の中でバランスのとり方がまだわかっていない。
    - 不等号についてはこれからも考えていこう。
    - `visited[row][col] == '1'` の部分は、自分としては一瞬島のことかと思ってしまった。
    - max 関数の中で関数呼び出しをしない方が読みやすそうかな
- https://github.com/t0hsumi/leetcode/pull/19/files
    - チェックをする処理のまとめ方について議論されている。一つにまとめたい気持ちもわかるな。
- https://github.com/ryoooooory/LeetCode/pull/21/files
    - そうか、スタックへの追加の処理をベタ書きするときも、関数を挟むと、追加する前にチェックができるのか。
- https://github.com/fhiyo/leetcode/pull/21/files
    - 再帰もありましたが、考えを整理する余裕がないのでこちらも後で整理しよう。

```python

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        WATER = 0
        num_rows = len(grid)
        num_cols = len(grid[0])
        seen = set()

        def add_land(next_lands, row, col):
            if not(0 <= row < num_rows and 0 <= col < num_cols):
                return 
            if grid[row][col] == WATER or (row, col) in seen:
                return
            next_lands.append((row, col))
            seen.add((row, col))

        def measure_island_area(start_row, start_col):
            next_lands = [(start_row, start_col)]
            seen.add((start_row, start_col))
            result = 0
            
            while next_lands:
                row, col = next_lands.pop()
                result += 1
                add_land(next_lands, row + 1, col)
                add_land(next_lands, row - 1, col)
                add_land(next_lands, row, col + 1)
                add_land(next_lands, row, col - 1)

            return result

        max_area = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == WATER or (row, col) in seen:
                    continue
                area = measure_island_area(row, col)
                max_area = max(max_area, area)

        return max_area

```

## Step3

- `WATER`の置き場所はどこが自然なのだろうか。
- とりあえず、この形で練習ができました。
- 範囲チェックは、自分が意図を込めているという感じがしていないので、他の人のコードを読みながら考えよう。

```python

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        num_rows = len(grid)
        num_cols = len(grid[0])
        seen = set()

        def is_visited_land(row, col):
            WATER = 0
            return grid[row][col] == WATER or (row, col) in seen

        def add_land(next_lands, row, col):
            if not(0 <= row < num_rows and 0 <= col < num_cols):
                return
            if is_visited_land(row, col):
                return
            next_lands.append((row, col))
            seen.add((row, col))

        def measure_island_area(start_row, start_col):
            next_lands = [(start_row, start_col)]
            seen.add((start_row, start_col))
            result = 0

            while next_lands:
                row, col = next_lands.pop()
                result += 1
                add_land(next_lands, row + 1, col)
                add_land(next_lands, row - 1, col)
                add_land(next_lands, row, col + 1)
                add_land(next_lands, row, col - 1)

            return result

        max_area = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if is_visited_land(row, col):
                    continue
                area = measure_island_area(row, col)
                max_area = max(max_area, area)

        return max_area

```
