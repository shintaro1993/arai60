# 617. Merge Two Binary Trees

- 二つの二分木をマージして、その二分木を返す。マージするとは言っても、入力で受け取った二分木は破壊しない方が自然な気がしている。
- 木の各ノードにおいて、右と左の子に、右部分木（左部分木）をマージして、部分木の参照を返して、という依頼をしていくことを考えました。

## Step1

- root1 or root2 が None の場合の処理で思っていたよりも行数が増えました。いくつか書き比べてみようと思います。

```python

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        sum_value = 0
        root1_left_child = None
        root1_right_child = None
        if root1:
            sum_value += root1.val
            root1_left_child = root1.left
            root1_right_child = root1.right

        root2_left_child = None
        root2_right_child = None
        if root2:
            sum_value += root2.val
            root2_left_child = root2.left
            root2_right_child = root2.right

        left_child = self.mergeTrees(root1_left_child, root2_left_child)
        right_child = self.mergeTrees(root1_right_child, root2_right_child)
        merged_root = TreeNode(sum_value, left_child, right_child)
        return merged_root

```

- 見積り
    - n: ノードの数
    - 時間計算量: O(n)
    - 空間計算量: O(n)

- 処理ごとに関数に分けてみましたが、もう少し他のやり方を考えたいです。

```python

class Solution:
    def get_sum_value(self, node1, node2):
        sum_value = 0
        if node1:
            sum_value += node1.val
        if node2:
            sum_value += node2.val
        return sum_value

    def get_left_children(self, node1, node2):
        node1_left_child = None
        node2_left_child = None
        if node1:
            node1_left_child = node1.left
        if node2:
            node2_left_child = node2.left
        return node1_left_child, node2_left_child

    def get_right_children(self, node1, node2):
        node1_right_child = None
        node2_right_child = None
        if node1:
            node1_right_child = node1.right
        if node2:
            node2_right_child = node2.right
        return node1_right_child, node2_right_child

    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        sum_value = self.get_sum_value(root1, root2)
        left_child = self.mergeTrees(*self.get_left_children(root1, root2))
        right_child = self.mergeTrees(*self.get_right_children(root1, root2))
        merged_root = TreeNode(sum_value, left_child, right_child)
        return merged_root

```

- root1 が None か root2 が None のときの場合分けをシンプルにしようと思い、番兵を使いました。メモリを追加で使用しますが、こちらが分かりやすく感じます。

```python

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None
        if root1 is None:
            root1 = TreeNode(0)
        if root2 is None:
            root2 = TreeNode(0)
        
        sum_value = root1.val + root2.val
        left_child = self.mergeTrees(root1.left, root2.left)
        right_child = self.mergeTrees(root1.right, root2.right)
        merged_root = TreeNode(sum_value, left_child, right_child)
        return merged_root

```

- stack を使うこともできそうですが、中身がわかりにくくなってきました。

```python

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        merged_root = TreeNode()
        merged_root_and_two_roots = [(merged_root, root1, root2)]
        while merged_root_and_two_roots:
            merged_node, node1, node2 = merged_root_and_two_roots.pop()
            if node1 is None and node2 is None:
                continue
            if node1 is None:
                node1 = TreeNode(0)
            if node2 is None:
                node2 = TreeNode(0)

            merged_node.val = node1.val + node2.val
            if node1.left or node2.left:
                merged_node.left = TreeNode()
            if node1.right or node2.right:
                merged_node.right = TreeNode()

            merged_root_and_two_roots.append((merged_node.left, node1.left, node2.left))
            merged_root_and_two_roots.append((merged_node.right, node1.right, node2.right))

        return merged_root    

```

## Step2

### 調べたこと・読んだコード

- https://discord.com/channels/1084280443945353267/1233603535862628432/1277243820118900847
    - Java には deepcopy がないんですね。
- https://discord.com/channels/1084280443945353267/1233603535862628432/1278020133628940395
- https://discord.com/channels/1084280443945353267/1262688866326941718/1297934906189549599
    - 関数への切り出し方がとてもシンプルでわかりやすい。後で書いてみよう。この視点も持っておきたい。
- c++ や他の言語との違いも整理しておこう
    - https://github.com/tarinaihitori/leetcode/pull/23#discussion_r1919824481
    - https://discord.com/channels/1084280443945353267/1350090869390311494/1364640007025070261
- https://github.com/colorbox/leetcode/pull/37/files
    - そうか、再帰呼び出しの前にノードを作っておくこともできますね。変数つくらなくてもいいですし、こちらの方が読みやすいかも。
- https://github.com/seal-azarashi/leetcode/pull/22
    - ループを使う場合で、ダミーノードを使わない方法について、c++ で書かれているが。
    - c++ だとそろそろ構造体を考え始めるのですね。
- https://github.com/Fuminiton/LeetCode/pull/23/files
    - いろいろ書き方あるけど、番兵を使った書き方が好きかもしれない。
- https://github.com/shining-ai/leetcode/pull/23
- https://github.com/hayashi-ay/leetcode/pull/12
    - new_node を3回書くのもいいですね。
    - deepcopy を使と読みやすくなっているのか。

- 自分がstep1の二つ目で書いたものよりは読む負担が少ないと思う。

```python

class Solution:
    def get_val(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return 0
        return node.val

    def get_left_child(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        return node.left

    def get_right_child(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        return node.right

    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        sum_value = self.get_val(root1) + self.get_val(root2)
        left_child = self.mergeTrees(self.get_left_child(root1), self.get_left_child(root2))
        right_child = self.mergeTrees(self.get_right_child(root1), self.get_right_child(root2))
        merged_root = TreeNode(sum_value, left_child, right_child)
        return merged_root 

```

- step1 の3番目に書いたものを修正したもの。
- まず入れ物を用意して、そこに詰めていく、と考えた方が自然かもしれない。

```python

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None
        if root1 is None:
            root1 = TreeNode(0)
        if root2 is None:
            root2 = TreeNode(0)
        
        merged_root = TreeNode()
        merged_root.val = root1.val + root2.val
        merged_root.left = self.mergeTrees(root1.left, root2.left)
        merged_root.right = self.mergeTrees(root1.right, root2.right)
        return merged_root 

```

- step1 で stack を使ったものを修正したもの。
- node1 と node2 のダミーノードの処理を関数に切り出すのが難しい。prepare_to_next_step を前半に持ってきてまとめておきたかったが。
- merged_node で merged_root の束縛を変更しようとしていた。ちゃんと整理しておこう。
    - https://docs.python.org/3/library/copy.html
        > Assignment statements in Python do not copy objects, they create bindings between a target and an object. 

```python

class Solution:
    def prepare_to_next_step(self, merged_node, node1, node2):
        if node1.left or node2.left:
            merged_node.left = TreeNode()
        if node1.right or node2.right:
            merged_node.right = TreeNode()

    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        merged_root = TreeNode()
        merged_root_and_two_roots = [(merged_root, root1, root2)]
        while merged_root_and_two_roots:
            merged_node, node1, node2 = merged_root_and_two_roots.pop()
            if node1 is None and node2 is None:
                continue
            if node1 is None:
                node1 = TreeNode(0)
            if node2 is None:
                node2 = TreeNode(0)

            merged_node.val = node1.val + node2.val
            self. prepare_to_next_step(merged_node, node1, node2)
            merged_root_and_two_roots.append((merged_node.left, node1.left, node2.left))
            merged_root_and_two_roots.append((merged_node.right, node1.right, node2.right))

        return merged_root 

```

- もし入力を破壊してもいいのであればこうもかけるのかな

```python

class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1

        root1.val += root2.val
        root1.left = self.mergeTrees(root1.left, root2.left)
        root1.right = self.mergeTrees(root1.right, root2.right)
        return root1

```

## Step3

- 書く練習をしていく中で、現状こちらのコードに落ち着きました。
- node と深さなどをタプルに詰めるのは自然だと思いましたが、今回はとりあえず詰めてしまった感がしてしまいました。考えるだけでは難しそうなので、やはりもっとコードを読んだ方がいいですね。

```python

class Solution:
    def create_left_if_needed(self, merged_node, node1, node2):
        if node1.left is not None or node2.left is not None:
            merged_node.left = TreeNode()

    def create_right_if_needed(self, merged_node, node1, node2):
        if node1.right is not None or node2.right is not None:
            merged_node.right = TreeNode()

    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None:
            return None

        merged_root = TreeNode()
        merged_roots_and_source_roots = [(merged_root, root1, root2)]
        while merged_roots_and_source_roots:
            merged_node, node1, node2 = merged_roots_and_source_roots.pop()
            if node1 is None and node2 is None:
                continue
            if node1 is None:
                node1 = TreeNode(0)
            if node2 is None:
                node2 = TreeNode(0)

            merged_node.val = node1.val + node2.val
            self.create_left_if_needed(merged_node, node1, node2)
            self.create_right_if_needed(merged_node, node1, node2)
            merged_roots_and_source_roots.append((merged_node.left, node1.left, node2.left))
            merged_roots_and_source_roots.append((merged_node.right, node1.right, node2.right))

        return merged_root

```
