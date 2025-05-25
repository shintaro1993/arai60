# 103. Binary Tree Zigzag Level Order Traversal

## Step1

- 入力データの二分木と出力用のリストを紙に並べて書いて考えてみる。
- 木の深さが偶数と奇数のときで処理を変える。

```python

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        zigzag_level_ordered_values = []
        nodes = [root]
        level = 0
        while nodes:
            next_level_nodes = deque()
            node_values = []
            for node in nodes:
                node_values.append(node.val)
                if level % 2 == 0:
                    next_level_nodes.appendleft(node.left)
                    next_level_nodes.appendleft(node.right)
                else:
                    next_level_nodes.appendleft(node.right)
                    next_level_nodes.appendleft(node.left)
            zigzag_level_ordered_values.append(node_values)
            level += 1
            nodes = [node for node in next_level_nodes if node is not None]
            
        return zigzag_level_ordered_values

```

- https://docs.python.org/3/library/collections.html#collections.deque

- 覚えやすくはないかもしれない。紙に絵を書けば再現できるが、読みやすくはないかもしれない。
- ごちゃごちゃ考えたが、レベルごとにノードをまとめて、結果として返すリストに追加するときに reverse する処理を追加した方が分かりやすい。
- https://docs.python.org/3/library/stdtypes.html#list
    > The reverse() method modifies the sequence in place for economy of space when reversing a large sequence. To remind users that it operates by side effect, it does not return the reversed sequence.

```python

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        zigzag_level_ordered_values = []
        nodes = [root]
        level = 0
        while nodes:
            node_values = []
            next_level_nodes = []
            for node in nodes:
                node_values.append(node.val)
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)
            if level % 2 != 0:
                node_values.reverse()
            zigzag_level_ordered_values.append(node_values)
            level += 1
            nodes = [node for node in next_level_nodes if node is not None]
        return zigzag_level_ordered_values

```

## Step2

### 調べたこと・読んだコード

- https://github.com/hayashi-ay/leetcode/pull/35
    - reverse させる方法が読みやすいですね。
    - level % 2 == 0 の方がいいのかな。
- https://github.com/shining-ai/leetcode/pull/27
    - 関数化するにしても人それぞれ違いがあるのが面白い。
    - level を -1 で初期化するのは好みじゃないかも
- https://github.com/sakupan102/arai60-practice/pull/28
    - reverse すると、ジグザグに traverse しているわけではないのでは、というコメントもありますね。
    - traverse 自体は左から行い、値のリストに deque を使う方法もあるのか。
- https://github.com/TORUS0818/leetcode/pull/29
    - reverse するかどうかをフラグで判定する方法も。
- https://github.com/Fuminiton/LeetCode/pull/27
    - 変数名はやっぱり悩ましいですね。
    - nodes の切り替えのときに 内法表記や filter を使っている人がいなかったので、if 文で書いた方が読みやすいのかもしれない。
    - cpython の実装を読んだりされている方がいると自分も頑張ろうと思える。
        - https://github.com/python/cpython/blob/main/Objects/listobject.c#L3169
        - https://github.com/python/cpython/blob/main/Objects/listobject.c#L1555


- step1の改善
- 一度 level order で作って、それを zigzag order に変換する方が個人的にわかりやすい気はする。

```python

class Solution:
    def converted_zigzag_order(self, level_ordered_values):
        zigzag_order = []
        for level, values in enumerate(level_ordered_values):
            if level % 2 != 0:
                values.reverse()
            zigzag_order.append(values)
        return zigzag_order

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        level_ordered_values = []
        nodes = [root]
        while nodes:
            next_level_nodes = []
            node_values = []
            for node in nodes:
                node_values.append(node.val)
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)
            level_ordered_values.append(node_values)
            nodes = [node for node in next_level_nodes if node is not None]
        return self.converted_zigzag_order(level_ordered_values)

```

- そうすると、while の中で node_values をなくした方が自然かな。

```python

class Solution:
    def converted_zigzag_order(self, level_ordered_values):
        zigzag_order = []
        for level, values in enumerate(level_ordered_values):
            if level % 2 != 0:
                values.reverse()
            zigzag_order.append(values)
        return zigzag_order

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        level_ordered_values = []
        nodes = [root]
        while nodes:
            level_ordered_values.append([])
            next_level_nodes = []
            for node in nodes:
                level_ordered_values[-1].append(node.val)
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)
            nodes = [node for node in next_level_nodes if node is not None]
        return self.converted_zigzag_order(level_ordered_values)

```

## Step3

- step2 のコードもいいと思ったが、level-order -> zigzag-level-order の流れよりも最初から zigzag で作った方が読む人は読みやすいと思いました。
- chromium のコードにも、'a % 2 != 0' の記述はあったので悪くはないかもしれないけど、関数にはしなくてもいいのかもしれない。どうしようか迷いました。

```python

class Solution:
    def is_odd(self, level):
        return level % 2 != 0

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        zigzag_level_ordered_values = []
        nodes = [root]
        level = 0
        while nodes:
            node_values = []
            next_level_nodes = []
            for node in nodes:
                node_values.append(node.val)
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)
            if self.is_odd(level):
                node_values.reverse()
            zigzag_level_ordered_values.append(node_values)
            level += 1
            nodes = [node for node in next_level_nodes if node is not None]
        return zigzag_level_ordered_values

```