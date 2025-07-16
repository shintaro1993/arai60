# 104. Maximum Depth of Binary Tree

- 右部分木の深さと左部分木の深さを受け取って、大きい方を1増やして親に返していくとよさそうかな。

## Step1

- 右部分木と左部分木の大きい方をインクリメントしながら親に返していく方法

```python

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return max(left_depth, right_depth) + 1

```

- 根から降りていくときにノードの数を数えていき、返るときに大きい方を返すということもできそう。

```python

class Solution:
    def get_depth(self, root, depth) -> int:
        if root is None:
            return depth
        left_depth = self.get_depth(root.left, depth + 1)
        right_depth = self.get_depth(root.right, depth + 1)
        return max(left_depth, right_depth)
        
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        return self.get_depth(root, 0)

```

- 2つめの方法を stack を使って書いたもの

```python

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        node_and_depths = [(root, 0)]
        max_depth = 0
        while node_and_depths:
            node, depth = node_and_depths.pop()
            if node is None:
                max_depth = max(max_depth, depth)
                continue
            node_and_depths.append((node.left, depth + 1))
            node_and_depths.append((node.right, depth + 1))
        return max_depth

```

### 見積り

- n: ノードの数
- 時間計算量: O(n)
- 空間計算量: O(n)
    - 木の形によっては n になる場合もある

- 1つ目の再帰の書き方が自分の中で直感的で書きやすいと感じた。再帰呼び出しを行える上限をどのように考えればいいかわからないが、場合によっては stack を使った書き方を選ぶかもしれない。自分の環境では、デフォルトでは上限が 1000 だった。
    - https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
- stack で書いたときの変数名を考え直したほうがいいかのかな。根から降りていくときは level の方があっているのか。

## Step2

### 調べたこと・読んだコード

- https://github.com/goto-untrapped/Arai60/pull/45#discussion_r1736098146
    - dfs で max 関数を使いながら下りていくよりは、bfs で maxDepth++ していく方が自然に感じるかな。
    - stack を使って、行きがけの処理と帰りがけの処理を管理する方法もある。
    - メモリのことを考えて、stack に None な node を積まないようにする選択肢もある。
- https://github.com/nittoco/leetcode/pull/14/files
    - 再帰呼び出しは一行にまとめるより二行に分けた方が読みやすいな。
- https://github.com/shining-ai/leetcode/pull/21/files
    - ここまで、level という単語は見ないので、depth でいいのかな。
    - 再帰を使って帰りがけに1を加える方法も複数ある。個人的には、自分が書いた方が好きかな。
- https://github.com/olsen-blue/Arai60/pull/21/files
    - やっぱり下りながら depth++ していくのが好きかもしれない。

- 下りながら max_depth をインクリメントする方法を書き比べてみる。

```python

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        max_depth = 0
        nodes = deque([root])
        while nodes:
            for _ in range(len(nodes)):
                node = nodes.popleft()
                if node.left:
                    nodes.append(node.left)
                if node.right:
                    nodes.append(node.right)
            max_depth += 1
        return max_depth

```

```python

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        max_depth = 0
        nodes = [root]
        while nodes:
            nodes_of_next_level = []
            for node in nodes:
                if node.left:
                    nodes_of_next_level.append(node.left)
                if node.right:
                    nodes_of_next_level.append(node.right)
            nodes = nodes_of_next_level
            max_depth += 1
        return max_depth

```

- deque を使うよりはリストを二つ使う方が自然に思えるかな。

## Step3

```python

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return max(left_depth, right_depth) + 1

```