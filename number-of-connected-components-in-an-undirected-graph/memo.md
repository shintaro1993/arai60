# Number of Connected Components in an Undirected Graph

## Step1

- 考えたこと
    - まとまりが何個あるか数える問題。
    - 作業中に発見済みと未発見のノードの情報を管理する。未発見のノードからたどれるノードをすべて発見済みにする、という作業を、未発見のノードがなくなるまで行った回数を求める。
    - 入力で辺の組のリストが与えられる。これを隣接リストか隣接行列に変更して、探索を行う。
    - 発見済みかどうかの情報は、set で管理しようか。
    - bfs でもできそうです。

- 入力の edges を 隣接リストに変換しました。
- リストを要素に持つリストとして g を初期化しておく。node1 と node2 をつなぐ辺があったとき、g[node1] に node2 を追加する。無効グラフなので逆も行う。
    - https://en.wikipedia.org/wiki/Adjacency_list

```python

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        seen = set()
        adjacency_list = [[] for _ in range(n)]
        for node1, node2 in edges:
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)

        def traverse(start_node: int) -> None:
            next_nodes = [start_node]
            seen.add(start_node)

            while next_nodes:
                node = next_nodes.pop()
                for neighbor in adjacency_list[node]:
                    if neighbor in seen:
                        continue
                    next_nodes.append(neighbor)
                    seen.add(neighbor)

        num_connected_components = 0
        for node in range(n):
            if node in seen:
                continue
            traverse(node)
            num_connected_components += 1

        return num_connected_components

```

- 最初要件を勘違いしていたが、存在しないノードはないということらしい。
- 関数の中の関数で、while for if が続くので、もう少し浅くした方がいいかそのままでいいか。あ

- 隣接行列を使う場合。
- 長さ n の行と、長さ n の列を持つように、リストを要素に持つリストとして g を初期化する。
- node1 と node2 をつなぐ辺があることを、g[node1][node2] == 1 と g[node2][node1] == 1 で表現する。
    - https://en.wikipedia.org/wiki/Adjacency_matrix

```python

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        seen = set()
        adjacency_matrix = [[0] * n for _ in range(n)]
        for node1, node2 in edges:
            adjacency_matrix[node1][node2] = 1
            adjacency_matrix[node2][node1] = 1

        def traverse(start_node: int) -> None:
            next_nodes = [start_node]
            seen.add(start_node)

            while next_nodes:
                node = next_nodes.pop()
                for neighbor in range(n):
                    if adjacency_matrix[node][neighbor] == 0:
                        continue
                    if neighbor in seen:
                        continue
                    next_nodes.append(neighbor)
                    seen.add(neighbor)

        num_connected_components = 0
        for node in range(n):
            if node in seen:
                continue
            traverse(node)
            num_connected_components += 1

        return num_connected_components

```

- 再帰の場合、関数の入り口でチェックをしたものが分かりやすく感じました。

```python

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        seen = set()
        adjacency_list = [[] for _ in range(n)]
        for node1, node2 in edges:
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)

        def traverse(node: int) -> None:
            if node in seen:
                return None
            seen.add(node)
            for neighbor in adjacency_list[node]:
                traverse(neighbor)

        num_connected_components = 0
        for node in range(n):
            if node in seen:
                continue
            traverse(node)
            num_connected_components += 1

        return num_connected_components

```

- 隣接リストと隣接行列の選択は discord 調べながら考えてみよう。
    - https://stackoverflow.com/questions/2218322/what-is-better-adjacency-lists-or-adjacency-matrices-for-graph-problems-in-c

## Step2

### 調べたこと・読んだコード

- https://discord.com/channels/1084280443945353267/1183683738635346001/1197650475160449025
    - Union Find について解説をしていただいているのであとで読もう。google docs は見れなくなっている。
- https://discord.com/channels/1084280443945353267/1200089668901937312/1212395962249781289
    - グラフの初期化に defaultdict を使うことは思いつきませんでした。
    - コードを読みにいくときの感覚。
    - 復習のときに、deque の中身を見ながら BFS でも書いてみよう
        - https://stackoverflow.com/questions/6256983/how-are-deques-in-python-implemented-and-when-are-they-worse-than-lists
            > 私は、deque の中身は、大体こんなもんだろうと覚えていて、上のスタックオーバーフロー見て、ついでにソースも斜め読みする、くらいするんですよ。で、このソースを読むの普通にするでしょう、という感覚なんですが
        > ただ、ローカルルールがあって合わせられることはできないと困るくらいの感覚です。
    - step5 の DFS BFS のコードは、どちらかというと DFS のイメージが強く残りました。 
- https://github.com/shining-ai/leetcode/pull/19
    - 隣接リストを作るとき同じ辺が複数来たときに、それを捨てるということを考えて list ではなく set を要素に持たせるのもいいかもですね。隣接するノードのことを自分は neighbor としましたが、スタックが next_nodes なので、合わせて next_node と置いてもいいかもしれない。
- https://discord.com/channels/1084280443945353267/1227073733844406343/1236915593974648872
    - defaultdict ではなく、list を使う方が定数倍高速化できる場合がある、というお題をいただいたので、後でその確認をしに行こう
        - https://github.com/sakupan102/arai60-practice/pull/22/files#r1590628823
    - 個人的には、訪問済みだとわかったら continue する方が好きですかね。
- https://discord.com/channels/1084280443945353267/1196472827457589338/1256559145033924678
    - node という変数名は改善の余地がありそうですが、もう少し考えたい。
- https://discord.com/channels/1084280443945353267/1233603535862628432/1260614366982574204
    - 訪問済みかどうかを管理する seen は list にする方法もあり。
- https://discord.com/channels/1084280443945353267/1239148130679783424/1348428159170773002
    - グラフを作るときに、from と to を使うのもいいですね。

- seen をリストにしようか迷いましたが、set での書き方の方が分かりやすくそのままにしました。
- 変数名だけ next_node に変えました。

```python

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        seen = set()
        adjacency_list = [[] for _ in range(n)]
        for node1, node2 in edges:
            adjacency_list[node1].append(node2)
            adjacency_list[node2].append(node1)

        def traverse(start_node: int) -> None:
            next_nodes = [start_node]
            seen.add(start_node)

            while next_nodes:
                node = next_nodes.pop()
                for next_node in adjacency_list[node]:
                    if next_node in seen:
                        continue
                    next_nodes.append(next_node)
                    seen.add(next_node)

        num_connected_components = 0
        for node in range(n):
            if node in seen:
                continue
            traverse(node)
            num_connected_components += 1

        return num_connected_components

```

## Step3

- step2 のコードで練習しました。

- 少しずつ余裕ができ、こういうときは何をした方がいいのかなどがすっと出てくるようになった気がする。
- cpython の実装を見に行くことも習慣にしていこう。

