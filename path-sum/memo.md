# 112. Path Sum

- パスの合計を管理しながら探索を行い、葉ノードで合計が targetSum と一致しているか調べてその結果を返していくとよさそう。

## Step1

- `targetSum - root.val == 0` が複数個所にあるのが気になる。

```python

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        if root.left is None and root.right is None:
            return targetSum - root.val == 0
        return self.hasPathSum(root.left, targetSum - root.val) or self.hasPathSum(root.right, targetSum - root.val)

```

- targetSum はパスの合計なので、一つのノードの値と一致しているか調べているのは違和感があるかも。

```python

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        if root.left is None and root.right is None:
            return root.val == targetSum
        targetSum -= root.val
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)

```

- target_sum というよりは、残ったものとして変数に入れた方が自然かな

```python

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        remaining_sum = targetSum - root.val
        if root.left is None and root.right is None:
            return remaining_sum == 0
        return self.hasPathSum(root.left, remaining_sum) or self.hasPathSum(root.right, remaining_sum)

```

- stack を使って書いてみる。パスの合計を計算していきながら葉ノードでtargetSumと一致しているか調べるのが自然だと感じる。

```python

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False

        nodes_and_path_sums = [(root, root.val)]
        while nodes_and_path_sums:
            node, path_sum = nodes_and_path_sums.pop()
            if node.left is None and node.right is None:
                if path_sum == targetSum:
                    return True
                continue
            if node.left:
                nodes_and_path_sums.append((node.left, path_sum + node.left.val))
            if node.right:  
                nodes_and_path_sums.append((node.right, path_sum + node.right.val))
        return False

```

## Step2

- https://github.com/olsen-blue/Arai60/pull/25/files
    - 再帰で、別の関数を用意するのもありかな。
- https://github.com/TORUS0818/leetcode/pull/27
    - stack で `if not node.left and not node.right and node.val == target_sum: return True` が使われているコードを読むのはいい練習になったかも。
- https://github.com/sakupan102/arai60-practice/pull/26
    - path_sum を0で初期化すると、stack に積むときの if 文をなくせていいですね。get_val 関数を用意して node が None の場合を処理させるよりいいかも。
- https://github.com/shining-ai/leetcode/pull/25
    - 葉ノードの処理のネストを浅くすると、個人的には逆に読みにくいかもしれない。他の方法はあるかな。
- https://github.com/hayashi-ay/leetcode/pull/30
    - 個人的には stack から取り出して足すより、入れるときに足した方が好きかも。

```python

class Solution:
    def has_no_child(self, node):
        return node.left is None and node.right is None

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False

        nodes_and_path_sums = [(root, 0)]
        while nodes_and_path_sums:
            node, path_sum = nodes_and_path_sums.pop()
            if node is None:
                continue
            path_sum += node.val
            if self.has_no_child(node):
                if path_sum == targetSum:
                    return True
                continue
            nodes_and_path_sums.append((node.left, path_sum))
            nodes_and_path_sums.append((node.right, path_sum))
        return False

```

## Step3

- 書いていると、葉ノードのところで continue しなくてもいいかなという気持ちになりました。

```python

class Solution:
    def has_no_child(self, node: Optional[TreeNode]) -> bool:
        return node.left is None and node.right is None

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False

        nodes_and_path_sums = [(root, 0)]
        while nodes_and_path_sums:
            node, path_sum = nodes_and_path_sums.pop()
            if node is None:
                continue
            path_sum += node.val
            if self.has_no_child(node) and path_sum == targetSum:
                return True
            nodes_and_path_sums.append((node.left, path_sum))
            nodes_and_path_sums.append((node.right, path_sum))
        return False

```