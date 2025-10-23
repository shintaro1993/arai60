# 847 · Split BST

## step1

二分探索木と v が与えられる。すべてのノードの値が v 以下を満たす二分探索木と v より大きいという条件を満たす二分探索木に分けて、ノードの数が多い方の二分探索木を返す。もし数が同じ場合、ルートの値の大きい方を返す。

上記の条件を満たすように二分探索木を分割する、それぞれの木のノードの数を数える、返却する条件を調べて結果を返す、というステップで考える。入力で受け取った二分探索木を壊さないように最初にコピーを作っておく。

分割処理をする関数について、戻り値として、v 以下の二分探索木の root と、v より大きい方二分探索木の root を返したい。処理について考える。
- node.val が v 以下の場合
    - node と左部分木は v 以下であるという条件を満たしている。右部分木には、v 以下の部分木と v より大きい部分木がある。v 以下の部分木を node の右部分木として更新して、これらをセットで返す。
- node.val が v より大きい場合
    - node と右部分木が v より大きいという条件を満たしている。左部分木には、v 以下の部分木と v より大きい部分木がある。v より大きい部分木を node の左部分木として更新して、これらをセットで返す。

もし関数の入力として None が渡された場合、例外を出すよりは None を返す方がいいかな。

```python

import copy
from typing import Optional


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def _count_nodes(self, root: TreeNode) -> int:
        if root is None:
            return 0
        count = 0
        nodes = [root]
        while nodes:
            next_nodes = []
            for node in nodes:
                count += 1
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return count

    def _split_bst_helper(self, root: TreeNode, v: int) -> list[Optional[TreeNode]]:
        if root is None:
            return [None, None]
        
        if root.val <= v:
            smaller_root, larger_root = self._split_bst_helper(root.right, v)
            root.right = smaller_root
            return [root, larger_root]
        else:
            smaller_root, larger_root = self._split_bst_helper(root.left, v)
            root.left = larger_root
            return [smaller_root, root]

    def split_b_s_t(self, root: TreeNode, v: int) -> Optional[TreeNode]:
        if root is None:
            return None
        
        copied_root = copy.deepcopy(root)
        smaller_root, larger_root = self._split_bst_helper(copied_root, v)
        num_smaller = self._count_nodes(smaller_root)
        num_larger = self._count_nodes(larger_root)
        
        if num_smaller > num_larger:
            return smaller_root
        return larger_root

```

n: ノードの数
n <= 50 を想定
時間計算量は O(n) で1秒以内には終わりそう。空間計算量 O(n) でメモリにものりそう。

smaller_root のすべてのノードの値 <= v < larger_root のすべてのノードの値であることを保証しているので、二つの二分探索木のノードの数が同じ場合は larger_root を返せばいい。smaller_root を返すのは num_smaller > num_larger のときだけなのでそこだけ先にチェックしておく。

https://docs.python.org/3/library/copy.html#copy.deepcopy
https://github.com/python/cpython/blob/c0f0eca4dac61f13b7d6c29c91853474a8b31b80/Lib/copy.py#L110

ループにするの苦労するな。

## step2

leetcode 版とは微妙に問題が違っていますね。

- https://github.com/tokuhirat/LeetCode/pull/47/files
    - 自分も関数の引数に tree を考えたが、木の根のことであれば root がわかりやすそうな気がしてきて難しい。
    - 再帰をループになおすとき、その中間を経由するという考えはいいかもしれない。
    - ループよりは再帰の方がわかりやすいかも。自分の step1 と似ているからかもしれないが。

- https://github.com/Ryotaro25/leetcode_first60/pull/50/files
    - c++ で書かれた、再帰の中間のようなコードは前も見た気がするけど、これを python のコードにするの苦手かもしれない。

- https://github.com/olsen-blue/Arai60/pull/48/files
    > child_smaller_root, child_larger_root = self.splitBST(root.right, target)
    - 自分の右部分木に対して子は一つの認識だけど、どうだろうか。
    - 変数名をもう少し見直していこうかな。

再帰をループになおすときに中間となるものを考える。（再帰の戻り値を使わない）
作業結果を親に報告できないので、あらかじめ作業場所を用意しておき、そこを使う。
子の作業結果が分からない状態で、一度だけ作業ができる。

今回の処理対象は木ではあるけど、探索というよりは降りていくイメージがあっているかも。

根視点で考えると、以下の作業を考える。
root.val <= v の場合、root.right を、右部分木における v 以下の値を持つ一番近くの子孫に繋ぎ変える必要がある。
root.val > v の場合、root.left を左部分木における v より大きい値を持つ一番近くの子孫に繋ぎ変える必要がある。

仕事を依頼された立場で考えると入力で受け取った二分探索木における、v 以下である一番近くの祖先と、v より大きい一番近くの祖先が分かっていれば、自分がどちらに属するか調べて更新し、子に依頼することができそう。これらをそれぞれ smaller と larger として、_split_bst_helper の引数にすることで、再帰の行きだけで処理をするような中間的なコードになりそう。

```python

import copy
from typing import Optional


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def _count_nodes(self, root: TreeNode) -> int:
        if root is None:
            return 0
        count = 0
        nodes = [root]
        while nodes:
            next_nodes = []
            for node in nodes:
                count += 1
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return count

    def _split_bst_helper(
        self, root: TreeNode, v: int, smaller: TreeNode, larger: TreeNode
    ) -> list[Optional[TreeNode]]:
        if root is None:
            return

        if root.val <= v:
            next_root = root.right
            root.right = None
            smaller.right = root
            self._split_bst_helper(next_root, v, smaller.right, larger)
        else:
            next_root = root.left
            root.left = None
            larger.left = root
            self._split_bst_helper(next_root, v, smaller, larger.left)

    def split_b_s_t(self, root: TreeNode, v: int) -> Optional[TreeNode]:
        if root is None:
            return None

        copied_root = copy.deepcopy(root)
        dummy_smaller_root = TreeNode(None)
        dummy_larger_root = TreeNode(None)
        self._split_bst_helper(copied_root, v, dummy_smaller_root, dummy_larger_root)
        num_smaller = self._count_nodes(dummy_smaller_root)
        num_larger = self._count_nodes(dummy_larger_root)

        if num_smaller > num_larger:
            return dummy_smaller_root.right
        return dummy_larger_root.left

```

これをループにする

```python

import copy
from typing import Optional


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def _count_nodes(self, root: TreeNode) -> int:
        if root is None:
            return 0
        count = 0
        nodes = [root]
        while nodes:
            next_nodes = []
            for node in nodes:
                count += 1
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return count

    def split_b_s_t(self, root: TreeNode, v: int) -> Optional[TreeNode]:
        if root is None:
            return None

        node = copy.deepcopy(root)
        dummy_smaller_root = TreeNode(None)
        dummy_larger_root = TreeNode(None)
        smaller_node = dummy_smaller_root
        larger_node = dummy_larger_root
        while node is not None:
            if node.val <= v:
                next_node = node.right
                node.right = None
                smaller_node.right = node
                smaller_node = smaller_node.right
                node = next_node
            else:
                next_node = node.left
                node.left = None
                larger_node.left = node
                larger_node = larger_node.left
                node = next_node

        num_smaller = self._count_nodes(dummy_smaller_root)
        num_larger = self._count_nodes(dummy_larger_root)

        if num_smaller > num_larger:
            return dummy_smaller_root.right
        return dummy_larger_root.left

```

変数名の整理が必要な気がするな。while ループの中の更新処理は他の書き方もあるので、時間をおいて見直してみよう。

## step3

step1 のコードで練習をしました。変更点は、_count_nodes 関数内の count と nodes の初期化の順番です。

```python

import copy
from typing import Optional


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def _count_nodes(self, root: TreeNode) -> int:
        if root is None:
            return 0
        count = 0
        nodes = [root]
        while nodes:
            next_nodes = []
            for node in nodes:
                count += 1
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            nodes = next_nodes
        return count

    def _split_bst_helper(self, root: TreeNode, v: int) -> list[Optional[TreeNode]]:
        if root is None:
            return [None, None]
        
        if root.val <= v:
            smaller_root, larger_root = self._split_bst_helper(root.right, v)
            root.right = smaller_root
            return [root, larger_root]
        else:
            smaller_root, larger_root = self._split_bst_helper(root.left, v)
            root.left = larger_root
            return[smaller_root, root]

    def split_b_s_t(self, root: TreeNode, v: int) -> Optional[TreeNode]:
        if root is None:
            return None
        
        copied_root = copy.deepcopy(root)
        smaller_root, larger_root = self._split_bst_helper(copied_root, v)
        num_smaller = self._count_nodes(smaller_root)
        num_larger = self._count_nodes(larger_root)

        if num_smaller > num_larger:
            return smaller_root
        return larger_root

```