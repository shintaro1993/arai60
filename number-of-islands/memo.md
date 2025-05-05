# 200. Number of Islands

## Step1

- 考えたこと
    - grid の中の island を water に変更する作業を、island がなくなるまで行い、それを行った回数を返す。
    - 渡した grid が変更されることをユーザーは意図していないと思うので、コピーを作ってそこで作業を行うか、それとも grid に変更を加えず作業の記録をどこかに保存しておく。

- 見積
    - 時間計算量：O(m * n)
    - 空間計算量：O(m * n)

- mutable なオブジェクトの参照を要素に持つリストなので、変更した内容がコピー元に影響を与えないように deepcopy を使います。
    - https://docs.python.org/3/library/copy.html

```python

class Solution:
    def convert_island_to_water(self, grid, start_row, start_col):
        next_lands = [(start_row, start_col)]
        grid[start_row][start_col] = "0"        

        while next_lands:
            row, col = next_lands.pop()
            for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row = row + d_row
                next_col = col + d_col
                if next_row < 0 or len(grid) <= next_row or next_col < 0 or len(grid[0]) <= next_col:
                    continue
                if grid[next_row][next_col] == "0":
                    continue
                next_lands.append((next_row, next_col))
                grid[next_row][next_col] = "0"

    def numIslands(self, grid: List[List[str]]) -> int:
        new_grid = copy.deepcopy(grid)
        result = 0

        for row in range(len(new_grid)):
            for col in range(len(new_grid[0])):
                if new_grid[row][col] == "0":
                    continue
                self.convert_island_to_water(new_grid, row, col)
                result += 1

        return result

```

- `next_lands` に追加するときの処理を関数に切り出しただけになってしまった。もっといい方法があるだろうか。

```python

class Solution:
    def is_valid_next(self, grid, next_row, next_col):
        if next_row < 0 or len(grid) <= next_row or next_col < 0 or len(grid[0]) <= next_col:
            return False
        if grid[next_row][next_col] == "0":
            return False
        return True

    def convert_island_to_water(self, grid, start_row, start_col):
        next_lands = [(start_row, start_col)]
        grid[start_row][start_col] = "0"        

        while next_lands:
            row, col = next_lands.pop()
            for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row = row + d_row
                next_col = col + d_col
                if self.is_valid_next(grid, next_row, next_col):
                    next_lands.append((next_row, next_col))
                    grid[next_row][next_col] = "0"

    def numIslands(self, grid: List[List[str]]) -> int:
        new_grid = copy.deepcopy(grid)
        result = 0

        for row in range(len(new_grid)):
            for col in range(len(new_grid[0])):
                if new_grid[row][col] == "0":
                    continue
                self.convert_island_to_water(new_grid, row, col)
                result += 1

        return result

```

- 訪問済みの land の管理方法を、grid ではなく 新しく用意した set に変える。
- `next_lands` に追加するときの確認が増えているのが気になるが。

```python

class Solution:
    def is_valid_next(self, grid, seen_lands, next_row, next_col):
        if next_row < 0 or len(grid) <= next_row or next_col < 0 or len(grid[0]) <= next_col:
            return False
        if grid[next_row][next_col] == "0":
            return False
        if (next_row, next_col) in seen_lands:
            return False
        return True

    def traverse_island(self, grid, seen_lands, start_row, start_col):
        next_lands = [(start_row, start_col)]
        seen_lands.add((start_row, start_col))

        while next_lands:
            row, col = next_lands.pop()
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

- 自分の頭の中を整理するために、疑似コードのようなものを残しています。

```

def island の数を数える(grid):
    island の数 = 0

    while grid の中に未発見の land が存在する:
        未発見の land を一つ選ぶ
        関数 island を探索する、を呼び出す # 選んだ land と、そこからたどれるすべての land を発見済みにする
        island の数 += 1

    return island の数

def island を探索する(land)
    探索予定の land のリストに land を入れて初期化する
    
    while 探索予定の land のリストが空ではない:
        land を一つ取り出す
        while land に隣接している、未発見の land が存在する:
            条件を満たす land を発見済みにして、探索予定のリストに追加する

```

- 他の書き方として、next_land のデータ構造を deque に変えて幅優先探索のように探索を行う方法と、再帰を使う方法を practice.md に書きました。

## Step2

### 調べたこと

- https://discord.com/channels/1084280443945353267/1201211204547383386/1213153863704776774
    - Union Find を使った書き方は後で整理しよう
- https://github.com/sakupan102/arai60-practice/pull/18/files
    - 自分も d_row を使っていたので、省略しないようにしよう。
    - 探索リストに入れてもいいかどうか調べるためのチェックを雑に関数に切り出してしまっていた。`inside_grid` などのように、切り出すと意図が伝わりやすいと感じた。
    - deepcopy するのとは別に、新しく True, False でリストを作る手もありますね。
- https://github.com/quinn-sasha/leetcode/pull/18/files#r1997497127
    - grid の範囲内チェックの参考。
- https://github.com/TORUS0818/leetcode/pull/19/files
    - delta_row などを使わず書き下すのもよさそう。
- https://github.com/Mike0121/LeetCode/pull/34/files
    - キューから pop したときに範囲チェックをして grid を変更する書き方もある。再帰の場合と while の場合で整理しておかないといけない。
- https://github.com/hayashi-ay/leetcode/pull/33/files
    - 2nd の一つ目の再帰のコードの書き方、for ループではなく再帰呼び出しを4つ書くのは思いつかなかったけど、自分もやりたくなってきました。
    - 2nd の二つ目のBFSのコードの書き方、set は使ってないけど、grid を変更するのが pop した直後だから、複数回キューに入るかもしれないのかな。
    - どこでチェックするのかで、訪問済みと発見済みを使い分けた方がよさそうだと感じた。
- https://github.com/sakupan102/arai60-practice/pull/18/files
    - 行と列の大きさを変数に置いた方が全体として読みやすく感じました。
- https://github.com/goto-untrapped/Arai60/pull/38/files
    - LAND と WATER を使い分けられていたが、自分の中では使い分けた方が自然なのかよくわからないな。

```python

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        WATER = "0"
        seen = set()
        num_rows = len(grid)
        num_cols = len(grid[0])

        def inside_grid(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols

        def can_visit_land(row, col):    
            return not (grid[row][col] == WATER or (row, col) in seen)

        def traverse_island(start_row, start_col):
            next_lands = [(start_row, start_col)]
            seen.add((start_row, start_col))

            while next_lands:
                row, col = next_lands.pop()
                for delta_row, delta_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_row = row + delta_row
                    next_col = col + delta_col
                    if not inside_grid(next_row, next_col):
                        continue
                    if not can_visit_land(next_row, next_col):
                        continue
                    next_lands.append((next_row, next_col))
                    seen.add((next_row, next_col))

        num_islands = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if not can_visit_land(row, col):
                    continue
                traverse_island(row, col)
                num_islands += 1

        return num_islands

```

## Step3

- 書く練習で、`can_visit_land` を `can_visit` に変更しました。

## 感想

- Union Find と、再帰を使った書き方の整理ができていないので、復習のときにやる。
- 疑似コードのようなものを書くのは意外と悪くなさそうかな。練習していこう。