# 105. Construct Binary Tree from Preorder and Inorder Traversal

考えたこと:
- preorder のリストのインデックスが0番の値を根ノードとして、インデックスを管理しつつ dfs で探索しながら木を作っていけそうだと思いました。
- 左の子のインデックスは作成中のノードのインデックス + 1でよさそうで、右の子のインデックスは作成中のノードのインデックスとその左の子の数 + 1で求められそう。
- inorder のリストにおける注目しているノードのインデックスを探して、そこを境に左部分木と右部分木の部分に分け、左の子の数を数える。

## Step1

```python

class Solution:
    def build_tree_helper(self, preorder, inorder, node_index):
        if not inorder:
            return None

        node = TreeNode()
        node.val = preorder[node_index]
        split_index = inorder.index(preorder[node_index])
        node.left = self.build_tree_helper(
            preorder, inorder[:split_index], node_index + 1
        )
        node.right = self.build_tree_helper(
            preorder, inorder[split_index + 1:], node_index + split_index + 1
        )
        return node

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        return self.build_tree_helper(preorder, inorder, 0)

```

見積り:
- 時間計算量: O(n^2)
- 空間計算量: O(n)

調べたこと
- index 関数
    - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
    - https://github.com/python/cpython/blob/ebf6d13567287d04683dab36f52cde7a3c9915e7/Objects/listobject.c#L3282

- もし preorder のリストに存在して inorder のリストに存在しない値がある場合、ValueError になる。問題はなさそう。
- これは stack を使って書くこともできそうかな。
- index 関数を使って split_index を求めているが、inorder のリストにおける値とインデックスの辞書を作っておくこともできそう。
- 右の子と左の子の関数呼び出し時に inorder のリストをスライスしているが、これは変数を使って表現できそうかな。

```python

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        value_to_split_index = {value: index for index, value in enumerate(inorder)}

        def build_tree_helper(node_index: int, low: int, high: int) -> Optional[TreeNode]:
            if low >= high:
                return None

            node = TreeNode()
            node.val = preorder[node_index]
            split_index = value_to_split_index[preorder[node_index]]
            left_size = split_index - low
            node.left = build_tree_helper(node_index + 1, low, split_index)
            node.right = build_tree_helper(node_index + left_size + 1, split_index + 1, high)
            return node

        return build_tree_helper(0, 0, len(preorder))

```

見積り:
- 時間計算量: O(n)
- 空間計算量: O(n)

- stack を使って実装してみる。

```python

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        value_to_split_index = {value: index for index, value in enumerate(inorder)}
        root = TreeNode()
        stack = [(root, 0, 0, len(preorder))]
        while stack:
            node, node_index, low, high = stack.pop()
            node.val = preorder[node_index]
            split_index = value_to_split_index[preorder[node_index]]
            left_size = split_index - low
            if low < split_index:
                node.left = TreeNode()
                stack.append((node.left, node_index + 1, low, split_index))
            if split_index + 1 < high:
                node.right = TreeNode()
                stack.append((node.right, node_index + left_size + 1, split_index + 1, high))
        return root

```

- low と high を left と right を使ったものにした方が読みやすくなるかも。
- 変数名を整理しないとかな

## Step2

### 調べたこと・読んだコード

- https://github.com/nittoco/leetcode/pull/37/files
    - 範囲を保存せずに、preorder のリストのノードを一つずつ木に挿入していくような方法もあるんですね。
    - ちょっと読み切れないので、後で読みかえそう。
- https://github.com/olsen-blue/Arai60/pull/29#discussion_r1948256437
    - 一つの関数だけで再帰をしていますね。preorder のリストも変更して、preorder[0] の値でノードを作れるようにしておくと、呼び出しでインデックス渡さなくてもよいですね。
    - nonlocal を使う方法もありますかね。
        - https://ja.wikipedia.org/wiki/%E5%8F%82%E7%85%A7%E9%80%8F%E9%81%8E%E6%80%A7
- https://github.com/hayashi-ay/leetcode/pull/43/files
    - やっぱり、node_index と split_index を足すとき、split_index を一度別の変数に置くのがいいですかね。
- https://github.com/TORUS0818/leetcode/pull/31/files
    - while True で root から下りながら value を挿入していく。
- https://github.com/fhiyo/leetcode/pull/31/files
    - この再帰は両端を指定しているのではなく、オフセットとサイズを使っているのかな。
    - stack で書くときは、node を作ったときに値もセットしている。
- inorder についてはまた後で整理しよう
    - https://discord.com/channels/1084280443945353267/1247673286503039020/1300957719074967603
    - https://discord.com/channels/1084280443945353267/1247673286503039020/1300957861614063616
    - https://discord.com/channels/1084280443945353267/1339428945845555252/1356001335186685993

- 個人的には、ノードを作って、右の子と左の子を作るための情報をそれぞれスタックに積んで dfs していくのが分かりやすく感じた。
- step1 で stack を使って書いたコードを改善する。
- stack の変数名で何を表現するといいのかわからなくなってくる。

```python

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        value_to_index_in_inorder = {value: index for index, value in enumerate(inorder)}
        root = TreeNode()
        # node, preorder index, inorder left bound, inorder right bound
        tree_info_stack = [(root, 0, 0, len(preorder))]
        while tree_info_stack:
            node, node_index, left_bound, right_bound = tree_info_stack.pop()
            node.val = preorder[node_index]
            split_index = value_to_index_in_inorder[preorder[node_index]]
            left_size = split_index - left_bound
            right_size = right_bound - split_index - 1
            if left_size > 0:
                node.left = TreeNode()
                left_child_index = node_index + 1
                tree_info_stack.append((node.left, left_child_index, left_bound, split_index))
            if right_size > 0:
                node.right = TreeNode()
                right_child_index = node_index + left_size + 1
                tree_info_stack.append((node.right, right_child_index, split_index + 1, right_bound))
        return root

```

- ノードを作ったときに val をセットしておくこともできるが、上の方が好きかな。

```python

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        value_to_index_in_inorder = {value: index for index, value in enumerate(inorder)}
        root = TreeNode(preorder[0])
        # node, preorder index, inorder left bound, inorder right bound
        tree_info_stack = [(root, 0, 0, len(preorder))]
        while tree_info_stack:
            node, node_index, left_bound, right_bound = tree_info_stack.pop()
            split_index = value_to_index_in_inorder[preorder[node_index]]
            left_size = split_index - left_bound
            right_size = right_bound - split_index - 1
            if left_size > 0:
                node.left = TreeNode()
                left_child_index = node_index + 1
                node.left.val = preorder[left_child_index]
                tree_info_stack.append((node.left, left_child_index, left_bound, split_index))
            if right_size > 0:
                node.right = TreeNode(preorder)
                right_child_index = node_index + left_size + 1
                node.right.val = preorder[right_child_index]           
                tree_info_stack.append((node.right, right_child_index, split_index + 1, right_bound))
        return root

```

## Step3

- こちらのコードで書く練習をしました。
- stack に積むものが増えていったときに、どんな選択肢が使われているのか調べていこうと思いました。

```python

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        value_to_index_in_inorder = {
            value: index for index, value in enumerate(inorder)
        }
        root = TreeNode()
        # node, preorder index, inorder left bound, inorder right bound
        tree_info_stack = [(root, 0, 0, len(preorder))]
        while tree_info_stack:
            node, node_index, left_bound, right_bound = tree_info_stack.pop()
            node.val = preorder[node_index]
            split_index = value_to_index_in_inorder[preorder[node_index]]
            left_size = split_index - left_bound
            right_size = right_bound - split_index - 1
            if left_size > 0:
                node.left = TreeNode()
                left_child_index = node_index + 1
                tree_info_stack.append(
                    (node.left, left_child_index, left_bound, split_index)
                )
            if right_size > 0:
                node.right = TreeNode()
                right_child_index = node_index + left_size + 1
                tree_info_stack.append(
                    (node.right, right_child_index, split_index + 1, right_bound)
                )
        return root

```

## 感想・課題

- 他の方法についてはあまり理解できたと感じなかったので、例外処理なども含めて、時間を置いて考える
- どのようにコメントが使われているか意識する。
