# 98. Validate Binary Search Tree

- 右と左の部分木が二分探索木で、根の値が左の子より大きく右の子より小さいことを、すべてのノードに対して行えばいいかなと思った。
- しかし、この方法だと、左部分木の中に根より大きい値を持つノードが、右部分木の中に根より小さい値を持つノードが含まれる場合に対応できていない。
- 紙に絵を書いて整理すると、根に対して、より小さい値(low)と、より大きい値(high)があるとする。左の子が取れる値の範囲は、low はそのままで high が根の値になったもの。右の子の値が取れる範囲は、low が根の値になったもので high はそのまま。このことを再帰的に探索しながら調べていく。

## Step1

- 見積り
    - n: ノードの数
    - m: 木の高さ
    - 時間計算量: O(n)
    - 空間計算量: O(m)

- low と high より、lower と upper がいいのかもしれない。

```python

import math


class Solution:
    def is_valid_bst_helper(
        self, root: Optional[TreeNode], lower: float, upper: float
    ) -> bool:
        if root is None:
            return True
        if not (lower < root.val < upper):
            return False
        return (
            self.is_valid_bst_helper(root.left, lower, root.val) 
            and self.is_valid_bst_helper(root.right, root.val, upper)
        )

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        return self.is_valid_bst_helper(root, lower=-math.inf, upper=math.inf)

```

- lower と upper の初期値として math.inf を使いました。int と float がありますが、型は float でいいのでしょうかね。
    - https://peps.python.org/pep-0484/
        - Union や | なんていうのもあるですね。
    - https://docs.python.org/3/library/math.html#math.inf

- stack で書く方がわかりやすいかな。

```python

import math


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:    
        nodes_and_ranges = [(root, -math.inf, math.inf)]
        while nodes_and_ranges:
            node, lower, upper = nodes_and_ranges.pop()
            if node is None:
                continue
            if not (lower < node.val < upper):
                return False
            nodes_and_ranges.append((node.left, lower, node.val))
            nodes_and_ranges.append((node.right, node.val, upper))
        return True

```

## Step2

### 調べたこと・読んだコード

- https://discord.com/channels/1084280443945353267/1192736784354918470/1235116690661179465
    - inorder でノードを取り出すこともできるのか。
    - yield from について、practice.md で整理しておく
- https://github.com/YukiMichishita/LeetCode/pull/8/files
    - 再帰で、return f() and g() で返すのではなく、片方を if not f(): return False と書くのも読みやすいですね。
- https://github.com/olsen-blue/Arai60/pull/28/files
    - 下から値の範囲をあげていくというのも思いつかなかった。イメージできなかったのでまた復習のときに考えてみよう。
    - int と float について、MIN_VALUE や MAX_VALUE を使いたいと思うほどではないという感じかな。
- https://github.com/shining-ai/leetcode/pull/28/files
    - デフォルト引数とキーワード引数だとどっちがいいのかな。
    - helper は関数名の先頭につけるのもあるのか
- https://github.com/TORUS0818/leetcode/pull/30/files#r1712609142
    - int と float が混ざる場合、型には int を指定するのがいいんですかね。int に統一するというのは float を使わないということなのかな。
    - inorder の再帰もできるのか。ちょっと読むのが大変だ。

- inorder の再帰も少し練習してみます。
- 読む練習が必要そう。step1 の再帰の方が好きかな。

```python

import math


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        prev_value = -math.inf

        def is_valid_bst_helper(root: Optional[TreeNode]) -> bool:
            nonlocal prev_value
            if root is None:
                return True

            if not is_valid_bst_helper(root.left):
                return False
            if root.val <= prev_value:
                return False
            prev_value = root.val
            if not is_valid_bst_helper(root.right):
                return False
            return True

        return is_valid_bst_helper(root)

```

- step1で書いた再帰より、個人的には and を取り除いた方が読みやすいかもしれない。

```python

import math


class Solution:
    def is_valid_bst_helper(
        self, root: Optional[TreeNode], lower: float, upper: float
    ) -> bool:
        if root is None:
            return True
        if not (lower < root.val < upper):
            return False
        if not self.is_valid_bst_helper(root.left, lower, root.val):
            return False
        return self.is_valid_bst_helper(root.right, root.val, upper)
        
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        return self.is_valid_bst_helper(root, lower=-math.inf, upper=math.inf)

```

## Step3

- こちらで練習しました。ranges よりは bounds の方がいいかなと思いました。

```python

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        nodes_and_bounds = [(root, -math.inf, math.inf)]
        while nodes_and_bounds:
            node, lower, upper = nodes_and_bounds.pop()
            if node is None:
                continue
            if not (lower < node.val < upper):
                return False
            nodes_and_bounds.append((node.left, lower, node.val))
            nodes_and_bounds.append((node.right, node.val, upper))
        return True

```

