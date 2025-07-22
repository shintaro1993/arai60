# 102. Binary Tree Level Order Traversal

- レベルごとに探索を行っていくとよさそうかな。
- 幅優先探索の最中で、レベルごとにノードの値をまとめて、返却用のリストに追加していく。

## Step1

- 二つのリストを使って幅優先探索を行う方法。
- 変数名は後で変えたくなるかも。

- 見積り
    - n: ノードの数
    - 時間計算量: O(n)
    - 空間計算量: O(n)

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        
        result = []
        nodes = [root]
        while nodes:
            node_values = []
            next_nodes = []
            for node in nodes:
                node_values.append(node.val)
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            result.append(node_values)
            nodes = next_nodes
        return result

```

- deque を使った方が分かりやすくなるかな。どうだろうか。

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        nodes = deque([root])
        while nodes:
            node_values = []
            for _ in range(len(nodes)):
                node = nodes.popleft()
                node_values.append(node.val)
                if node.left is not None:
                    nodes.append(node.left)
                if node.right is not None:
                    nodes.append(node.right)
            result.append(node_values)
        return result

```

## Step2

### 調べたこと・読んだコード

- https://github.com/sakupan102/arai60-practice/pull/27/files
    - 長くなるけど、result は level_orderd_node_vals の方がわかりやすいかな。
    - while の頭で空のリストを返却用のリストに追加して、内側のループで、result[-1].append(node.val) のように値を追加していく方法もある。個人的には -1 はあんまり使いたくない気がする。
- https://github.com/TORUS0818/leetcode/pull/28/files
    - 自分は deque を使わない方が好きかもしれない。
- https://github.com/olsen-blue/Arai60/pull/26
    - depth は使わないがわかりやすさのために管理しているのかな。個人的にはリストなどの変数名で何とかしたい気持ちがある。
- https://github.com/Mike0121/LeetCode/pull/7
    - 読む人にとって必要な情報を整理して、それを変数名にしよう。
- https://github.com/hayashi-ay/leetcode/pull/32/files
    - level_order より、level_orderd の方が自然なのでしょうかね。
- https://github.com/Fuminiton/LeetCode/pull/26/files
    - なるほどです。filter を使って next_nodes から None を取り除くと、追加するときの if 文を取り除けますね。
    - built-in にあること気づいてませんでした。内法表記、ジェネレータ式でも書けるそうですね。
        - https://docs.python.org/3/library/functions.html#filter

- やっぱり今回は result じゃない方がいいかも。

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        
        level_ordered_values = []
        nodes = [root]
        while nodes:
            node_values = []
            next_level_nodes = []
            for node in nodes:
                node_values.append(node.val)
                if node.left is not None:
                    next_level_nodes.append(node.left)
                if node.right is not None:
                    next_level_nodes.append(node.right)
            level_ordered_values.append(node_values)
            nodes = next_level_nodes
        return level_ordered_values

```

- -1 がちょっと気になるけど、これは見慣れていないだけなのかな。それ以外はいい感じですが。

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        
        level_ordered_values = []
        nodes = [root]
        while nodes:
            level_ordered_values.append([])
            next_level_nodes = []
            for node in nodes:
                level_ordered_values[-1].append(node.val)
                if node.left is not None:
                    next_level_nodes.append(node.left)
                if node.right is not None:
                    next_level_nodes.append(node.right)
            nodes = next_level_nodes
        return level_ordered_values

```

- 個人的には filter より内法表記が好みかも。ただ変数名を考えるのが大変。

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        
        level_ordered_values = []
        nodes = [root]
        while nodes:
            node_values = []
            next_level_nodes = []
            for node in nodes:
                node_values.append(node.val)
                next_level_nodes.append(node.left)
                next_level_nodes.append(node.right)
            level_ordered_values.append(node_values)
            nodes = [node for node in next_level_nodes if node]
        return level_ordered_values

```

## Step3

- 個人的にはこの形が疲れにくいと思いました。

```python

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
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
            nodes = [node for node in next_level_nodes if node]
        return level_ordered_values

```