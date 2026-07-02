# 111. Minimum Depth of Binary Tree

- 木構造で考えたとき、右の部分木と左部分木における minimum depth を受け取り、小さい方をインクリメントして親に返すということを考えました。
- 木がない場合は深さが0になるので0を返すようにしても大丈夫そうだが、その場合受け取り側では、片方だけ0が返ってきたときにその0を使わないようにしないといけないと思う。
- まず、再帰で行きがけで深さを更新していく方法と、帰りがけで深さを更新していく方法を考えて、それを stack に書き換えたものでやってみる。
- 根から降りながら minimum depth を見つけるイメージでもできるかな。深さ順に探索を行い、一番最初に葉ノードを見つけたときに探索を打ち切って大丈夫そう。

## Step1

### approach1

- 右部分木と左部分木における minimum depth を受け取って、処理を行い、親に返していくという考えで書きました。
- 帰るときの処理について、葉ノードの場合、左の子がいない場合、右の子がいない場合、それ以外の場合で処理を分けました。
- 0を、子がいるかどうかのチェックにも使っています。場合分けはもう少し簡潔にできそうな気がします。

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        left_depth = self.minDepth(root.left)
        right_depth = self.minDepth(root.right)

        if left_depth == 0 and right_depth == 0:
            return 1
        if left_depth == 0:
            return right_depth + 1
        if right_depth == 0:
            return left_depth + 1
        return min(left_depth, right_depth) + 1

```

- if 文を一つ減らしたもの

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        left_depth = self.minDepth(root.left)
        right_depth = self.minDepth(root.right)

        if left_depth == 0 and right_depth != 0:
            return right_depth + 1
        if left_depth != 0 and right_depth == 0:
            return left_depth + 1
        return min(left_depth, right_depth) + 1

```

- 帰り際の処理を一部関数に切り出しました。引数の順番などもう少し考えたいです。

```python

class Solution:
    def has_only_left_child(self, node: Optional[TreeNode], left_depth: int, right_depth: int) -> bool:
        return left_depth != 0 and right_depth == 0

    def has_only_right_child(self, node: Optional[TreeNode], left_depth: int, right_depth: int) -> bool:
        return left_depth == 0 and right_depth != 0

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        left_depth = self.minDepth(root.left)
        right_depth = self.minDepth(root.right)

        if self.has_only_left_child(root, left_depth, right_depth):
            return left_depth + 1
        if self.has_only_right_child(root, left_depth, right_depth):
            return right_depth + 1
        return min(left_depth, right_depth) + 1

```

### approach2

- 行きがけに depth を更新していく処理を再帰で書きました。

```python

class Solution:
    def get_depth(self, root: Optional[TreeNode], depth: int) -> int:
        if root is None:
            return depth
        
        depth += 1
        left_depth = self.get_depth(root.left, depth)
        right_depth = self.get_depth(root.right, depth)

        if left_depth == depth and right_depth == depth:
            return depth
        if left_depth == depth:
            return right_depth
        if right_depth == depth:
            return left_depth
        return min(left_depth, right_depth)

    def minDepth(self, root: Optional[TreeNode]) -> int:
        return self.get_depth(root, 0)

```

- 処理を関数に切り出しました。こちらももう少し引数を整理できればいいなと感じました。

```python

class Solution:
    def has_only_left_child(self, node: Optional[TreeNode], left_depth: int, right_depth: int, depth: int) -> bool:
        return left_depth != depth and right_depth == depth

    def has_only_right_child(self, node: Optional[TreeNode], left_depth: int, right_depth: int, depth: int) -> bool:
        return left_depth == depth and right_depth != depth

    def get_depth(self, root: Optional[TreeNode], depth: int) -> int:
        if root is None:
            return depth
        
        depth += 1
        left_depth = self.get_depth(root.left, depth)
        right_depth = self.get_depth(root.right, depth)

        if self.has_only_left_child(root, left_depth, right_depth, depth):
            return left_depth
        if self.has_only_right_child(root, left_depth, right_depth, depth):
            return right_depth
        return min(left_depth, right_depth)

    def minDepth(self, root: Optional[TreeNode]) -> int:
        return self.get_depth(root, 0)

```

- 下のコードは動きません。depth をどこで更新するか注意していませんでした。

```python

class Solution:
    def get_depth(self, root: Optional[TreeNode], depth: int) -> int:
        if root is None:
            return depth
        
        left_depth = self.get_depth(root.left, depth + 1)
        right_depth = self.get_depth(root.right, depth + 1)

        if left_depth == depth and right_depth == depth:
            return depth
        if left_depth == depth:
            return right_depth
        if right_depth == depth:
            return left_depth
        return min(left_depth, right_depth)

    def minDepth(self, root: Optional[TreeNode]) -> int:
        return self.get_depth(root, 0)

```

- ここで、depth を行きがけに更新することと、末尾再帰であることを混同していたなと思いました。
- 上記は末尾再帰ではないと思うので、これを機械的に stack を使った書き方に変えるには、行きがけの状態と帰りがけの状態を stack に、別々に積んでいく必要があると思いました。

### approach3

- dfs で探索を行い、葉ノードを見つけたら depth を更新していくということを考えました。
- math.inf と float('inf') は output が Equivalent とのこと。
    - https://docs.python.org/3/library/math.html#math.inf

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        min_depth = float('inf')
        nodes_and_depths = [(root, 1)]
        while nodes_and_depths:
            node, depth = nodes_and_depths.pop()
            if node is None:
                continue
            if node.left is None and node.right is None:
                min_depth = min(min_depth, depth)
                continue
            nodes_and_depths.append((node.left, depth + 1))
            nodes_and_depths.append((node.right, depth + 1))
        return min_depth

```

### approach4

- 深さごとに探索を行い、葉ノードを見つけたら探索を打ち切るということを考えて書きました。

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes = [root]
        depth = 1
        while nodes:
            nodes_of_next_depth = []
            for node in nodes:
                if node is None:
                    continue
                if node.left is None and node.right is None:
                    return depth
                nodes_of_next_depth.append(node.left)
                nodes_of_next_depth.append(node.right)
            nodes = nodes_of_next_depth
            depth += 1

```

- for 文の中を書き換えた方が説明しやすくなった気がします。

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes = [root]
        depth = 1
        while nodes:
            nodes_of_next_depth = []
            for node in nodes:
                if node.left is None and node.right is None:
                    return depth
                if node.left:
                    nodes_of_next_depth.append(node.left)
                if node.right:
                    nodes_of_next_depth.append(node.right)
            nodes = nodes_of_next_depth
            depth += 1

```

- deque を使いました。分けて書くこともできますが、個人的にはノードと深さを一緒に持っていた方が好きかもしれません。

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes_and_depths = deque([(root, 1)])
        while nodes_and_depths:
            node, depth = nodes_and_depths.popleft()
            if node.left is None and node.right is None:
                return depth
            if node.left:
                nodes_and_depths.append((node.left, depth + 1))
            if node.right:
                nodes_and_depths.append((node.right, depth + 1))

```

- 葉ノードかどうかを調べる関数の名前に、is_leaf が思い浮かんだが。has_no_child の方がいいだろうか。

```python

class Solution:
    def is_leaf(self, node: Optional[TreeNode]) -> bool:
        return node.left is None and node.right is None

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes_and_depths = deque([(root, 1)])
        while nodes_and_depths:
            node, depth = nodes_and_depths.popleft()
            if self.is_leaf(node):
                return depth
            if node.left:
                nodes_and_depths.append((node.left, depth + 1))
            if node.right:
                nodes_and_depths.append((node.right, depth + 1))

```

## Step2

### 調べたこと・読んだコード

- https://github.com/sakupan102/arai60-practice/pull/23/files
    - depth は1で初期化する方が好きかなと思いました。
- https://github.com/olsen-blue/Arai60/pull/22/files
    - 自分で elif を使うことがあまりないので、書く練習や読む練習が必要だと感じた。
    - キューやスタックの名前の好みはまだ固まってないかもしれない。
    - 再帰の場合、戻り値を変数に置かない方法もある。
- https://github.com/usatie/leetcode/pull/4/files
    - テストの方法についての議論もある。自分も少しずつ考えていこう。
    - 自分は 1 + right より、right + 1 の方が好きかな。
- https://github.com/fhiyo/leetcode/pull/24/files
    - node_with_depth と node_and_depth の複数形についての議論があった。自分でも少し混乱してきた。そもそもリストの場合に、s をつける以外にはどのようなものがあるのだろうか。
- https://github.com/hayashi-ay/leetcode/pull/26/files
    - `unreachable` という例外を投げた方がいいのか。pep8 で具体的にどうすればいいか書かれているところが見つけられなかったので、チームの方針に合わせると考えておこう。
        - https://peps.python.org/pep-0008/#programming-recommendations
- https://github.com/t0hsumi/leetcode/pull/22/files
    - 再帰の葉ノードの判定の仕方は、`if root.left is None and root.right is None` の方が自然かもしれない。こちらを参考に step2 で再帰を書き直してみよう。
    - while を True で書く話がある。

- Step1の、帰りがけに深さを更新していくコードを修正しました。補助関数はなくてもいいかもしれません。
- 判定で0を使うより、こちらの方が分かりやすい気がします。自分の一番最初に考えたものに引っ張られすぎないようにしようと思いました。

```python

class Solution:
    def has_only_left_child(self, node: Optional[TreeNode]) -> bool:
        return node.left is not None and node.right is None

    def has_only_right_child(self, node: Optional[TreeNode]) -> bool:
        return node.left is None and node.right is not None

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        if self.has_only_left_child(root):
            return self.minDepth(root.left) + 1
        if self.has_only_right_child(root):
            return self.minDepth(root.right) + 1
        return min(self.minDepth(root.left), self.minDepth(root.right)) + 1

```

- while のところは True の方が読むときの負担を減らせるかもしれないと感じました。
- depth はリストの外に置いた方が、リストの変数名での悩みを減らせる気がしました。

```python

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes = [root]
        depth = 1
        while True:
            nodes_in_next_depth = []
            for node in nodes:
                if node.left is None and node.right is None:
                    return depth
                if node.left:
                    nodes_in_next_depth.append(node.left)
                if node.right:
                    nodes_in_next_depth.append(node.right)
            nodes = nodes_in_next_depth
            depth += 1

```

- 見積り
    - n: ノードの数
    - 時間計算量: O(n)
    - 空間計算量: O(n)

## Step3

- 練習をしていくうちに、こちらのコードに落ち着きました。

```python

class Solution:
    def has_no_child(self, node: Optional[TreeNode]) -> bool:
        return node.left is None and node.right is None

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        nodes = [root]
        depth = 1
        while True:
            nodes_in_next_depth = []
            for node in nodes:
                if node is None:
                    continue
                if self.has_no_child(node):
                    return depth
                nodes_in_next_depth.append(node.left)
                nodes_in_next_depth.append(node.right)
            nodes = nodes_in_next_depth
            depth += 1

```