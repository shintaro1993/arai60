# 63. Unique Paths II

## step1

num_paths[row][column] に、スタート地点からある地点(row, column)までの経路の数を保存しておき、num_paths[row][column] = num_paths[row - 1][column] + num_paths[row][column - 1] のように、過去の状態を使って現在の状態を求めていけばよさそうだと思う。
入力のリストが空の場合とゴールまで到達できない場合に0を返しているが、リストが空の場合は例外を投げるのも選択肢かな。num_paths の初期化をどこでやるかは分かれそうかな。
この考えで書いてみました。(./step1/approach_a.py)

m = obstacleGrid の長さ
n = obstacleGrid[i] の長さ
とすると、時間計算量 O(mn)、空間計算量 O(mn)

## step2

### 読んだコード

- https://github.com/sakupan102/arai60-practice/pull/35/files
    - row と column が 0 の場合を二重ループの外で処理しない方法もあり、参考になった。
    - スタート地点に障害物がある場合などははやめに return したいと思った。

- https://github.com/YukiMichishita/LeetCode/pull/15/files
    - リストをすべて1で初期化はしない方が好みかな。

- https://github.com/fhiyo/leetcode/pull/35/files
    > 1 の後に 0 が続いた時も値が変わらない計算をしてしまうので、else break を入れるといいのかなと思いました。
    - これは確かにそうかも。
    - リストを一次元にする方法もあるので練習してみよう。

- https://github.com/olsen-blue/Arai60/pull/34/files
    - OBSTACLE の位置を考えよう。
    - step3 が自分と似た考えだなと感じた。二重ループの中で `num_of_paths[r][c]` を計算するところのネストが浅くなっているのはいいなと思った。
    - 自分は obstacleGrid[r][c] の直前が OBSTACLE かどうかを見ていたが、obstacleGir[r][c] で判断すると見通しが良くなりそう。

- https://github.com/saagchicken/coding_practice/pull/20/files
    - `num_paths[0][0] = 1` をして、二重ループに入っていくのはシンプルでいいですね。

- https://github.com/Fuminiton/LeetCode/pull/34/files
    - 現在の場所が OBSTACLE かどうかでやっている方がやっぱりわかりやすい。

### 改善

step1 のコードを修正しました。(./step2/approach_b.py)
continue を break に変えるのは自然だと思いますが、途中で切り上げるのであれば、`num_paths[0][0] = 1` で二重ループに入りたいと思うようになりました。

上記の修正案をもとに書きました。(./step2/approach_c.py)
row と column がそれぞれ0の場合、ループの中で何もしないのが少し気になりますが、この形の方が自然に思えました。

num_paths を一次元にする方法も練習してみる。(./step2/approach_d.py)
OBSTACLE を見つけたらそこを0にすること。

## step3

approach_e.py のコードで練習しました。
row と column は、それぞれ r と c もありかもしれない。

```python

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

```

