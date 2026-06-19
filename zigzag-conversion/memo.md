# 6. Zigzag Conversion

## step1

ある文字列があって、それが zigzag pattern になった状態で渡される。それをもとの文字列に変換したものを返す。
zigzag pattern の文字列があって、それを行で分類して1行目からつなげていったものを返すという理解をしました。
行で分類することを考えたときに、s[0] は1行目、s[1] は2行目となっていきs[numRows] が numRows 行目になり、その次の s[numRows + 1] は numRows - 1 行目になり、これを1行目から numRows 行目までの範囲で繰り返していく。リストを numRows 個用意して、それぞれの文字を対応する行のリストに追加していき、最後につなげれば大丈夫そうか。

制約:
- 1 <= s.length <= 1000
- s は English letters (lower-case and upper-case) と ','、 '.' で構成される。
- 1 <= numRows <= 1000

rumRows が1の場合や s.length <= numRows の場合は s をそのまま返してもよさそう。

```python

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s
        
        rows = [[] for _ in range(numRows)]
        row_index = 0
        direction = 1
        for c in s:
            rows[row_index].append(c)

            if row_index == 0:
                direction = 1
            elif row_index == numRows - 1:
                direction = -1
            row_index += direction

        rows = ["".join(row) for row in rows]
        return "".join(rows)

```

ループの先頭で、注目している文字に対して格納する行のインデックスが用意されているようにする。格納する行は、0 <= row_index <= numRows - 1 を行ったり来たりしているので、次の準備をするときに、row_index が0のときは directin は1、numRows - 1 のときは -1 にするというように、範囲外に出ないようにするイメージが自分の中でわかりやすいと思った。ただ、numRows == 1 の場合は次が範囲外になるので、先に返しておく。

n: 文字列 s の長さ
時間計算量: O(n)
- Python で、だいたい0.001秒くらいで考えておく。
空間計算量: O(n)

## step2

- https://github.com/Mike0121/LeetCode/pull/26/files
    - 各ループの中で、正と負の方向にインデックスを動かしていく考えもある。
    - 自分は if row_index == 0, if row_index == numRows - 1 の順番が好きかな。

- https://github.com/fhiyo/leetcode/pull/58/files
    - 最後の処理をどのように書くと読みやすいか。for 文で join しながらリストに入れていって、最後 join するのもよさそうか。
    - 1と2だったら2の方が好きかもしれない。
        1. `return ''.join(''.join(row) for row in zigzag_rows)`
        2. `return ''.join(map(lambda row: ''.join(row), zigzag_rows))`

- https://github.com/hayashi-ay/leetcode/pull/71/files
    - この形もあるのですね。気持ち的には step を更新して current_row を更新したいかも。

```python

intermediates[current_row].append(c)
current_row += step
if current_row == 0 or current_row == num_rows - 1:
    step *= -1

```

- https://github.com/olsen-blue/Arai60/pull/61/files
    - フラグを反転させるための条件は or で繋ぐより分けた方が読みやすいのと、not より True False を代入した方が読みやすい。

進む方向をフラグで管理する方法。フラグを使うことで読みやすくなった気はあまりしなかったかも。最後のは for で回すのが読みやすいと思った。

```python

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s
        
        rows = [[] for _ in range(numRows)]
        row_index = 0
        going_down = True
        for c in s:
            rows[row_index].append(c)

            if row_index == 0:
                going_down = True
            if row_index == numRows - 1:
                going_down = False
            
            if going_down:
                row_index += 1
            else:
                row_index -= 1

        result = []
        for row in rows:
            result.append("".join(row))
        return "".join(result)

```

行が、0, 1, 2, 3, 2, 1, 0, 1, ... と続いていったとき、0から始まって次の0の直前までを一区切りとする。i 番目の文字に対して、i % cycle をしてインデックスの計算をする方法。
fhiyo さんのところで、if 文の中で row_index を用意していたのを外に出したいと思って以下のように変形させたが、`row_index = cycle - row_index` の形はどうなんだろうか、何とも言えない。
step1 の方が好みか。

```python

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s
        
        rows = [[] for _ in range(numRows)]
        cycle = 2 * (numRows - 1)
        for i, c in enumerate(s):
            row_index = i % cycle
            if numRows <= row_index:
                row_index = cycle - row_index
            rows[row_index].append(c)

        result = []
        for row in rows:
            result.append("".join(row))
        return "".join(result)

```

```python

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s
        
        rows = [[] for _ in range(numRows)]
        cycle = 2 * (numRows - 1)
        for i, c in enumerate(s):
            position = i % cycle
            row_index = min(position, cycle - position)
            rows[row_index].append(c)

        result = []
        for row in rows:
            result.append("".join(row))
        return "".join(result)

```

そういえばさっきよくわからないと思っていた itertools.bached のコードはこれを変形させるといけそう。
    - https://github.com/olsen-blue/Arai60/pull/61/files#r2040670667
    - https://docs.python.org/3/library/itertools.html#itertools.batched
        - version 3.12 から

## step3

このコードで練習しました。

```python

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s
        
        rows = [[] for _ in range(numRows)]
        row_index = 0
        direction = 1
        for c in s:
            rows[row_index].append(c)

            if row_index == 0:
                direction = 1
            elif row_index == numRows - 1:
                direction = -1
            row_index += direction

        result = []
        for row in rows:
            result.append("".join(row))
        return "".join(result)

```
