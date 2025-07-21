# 108. Convert Sorted Array to Binary Search Tree

- 受け取ったリストはソートされているので、真ん中の値で根ノードを作ってもよさそう。
- 根ノードを除き、リストを二つに分割して再帰的に繰り返せば、リスト内の各要素の二分探索木における位置が分かると思う。

## Step1

- 見積り
    - 時間計算量: O(nlogn)
    - 空間計算量: O(n)

```python

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None

        node = TreeNode()
        index = len(nums) // 2
        node.val = nums[index]
        node.left = self.sortedArrayToBST(nums[:index])
        node.right = self.sortedArrayToBST(nums[index + 1:])
        return node

```

- リスト自体を分割せずに変数を二つ用意して区間を管理することもできると思いました。

- 見積り
    - 時間計算量: O(n)
    - 空間計算量: O(n) 

```python

class Solution:
    def sorted_array_to_bst_helper(self, nums: List[int], left: int, right: int) -> Optional[TreeNode]:
        if left >= right:
            return None

        node = TreeNode()
        middle = (left + right) // 2
        node.val = nums[middle]
        node.left = self.sorted_array_to_bst_helper(nums, left, middle)
        node.right = self.sorted_array_to_bst_helper(nums, middle + 1, right)
        return node

    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        return self.sorted_array_to_bst_helper(nums, 0, len(nums))

```

- 再帰を使わない方法で書く。

- 見積り
    - 時間計算量: O(n)
    - 時間計算量: O(n)

```python

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        root = TreeNode()
        root_and_indexes = [(root, 0, len(nums))]
        while root_and_indexes:
            node, left, right = root_and_indexes.pop()
            middle = (left + right) // 2
            if left >= right:
                continue
            if left < middle:
                node.left = TreeNode()
            if middle + 1 < right:
                node.right = TreeNode()
            node.val = nums[middle]
            root_and_indexes.append((node.left, left, middle))
            root_and_indexes.append((node.right, middle + 1, right))
        return root

```

## Step2

### 調べたこと・読んだコード

- https://github.com/colorbox/leetcode/pull/38/files
    - indexes よりは、ranges の方がいいかもしれない。
    - 空間計算量の話はまた後で整理しておく。
- https://github.com/TORUS0818/leetcode/pull/26/files
    - 中身を詰めるより前に、入れ物だけ繋げておくのは面白いと思った。
- https://github.com/sakupan102/arai60-practice/pull/25/files
    - 自分は、0 と len(nums) で始めるのが好きだと思った。
- https://github.com/hayashi-ay/leetcode/pull/29
    - sentinel を使うという発想もあるのか。
- https://github.com/shining-ai/leetcode/pull/24/files
    - stack を使う実装について、自分ももう少し if 文の場所を変えたりしてみようかな。

- while が終了するときのことを考えると、if 文で continue して while が終わるより、下の方が素直かな？

```python

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        root = TreeNode()
        root_and_indexes = [(root, 0, len(nums))]
        while root_and_indexes:
            node, left, right = root_and_indexes.pop()
            middle = (left + right) // 2
            node.val = nums[middle]
            if left < middle:
                node.left = TreeNode()
                root_and_indexes.append((node.left, left, middle))
            if middle + 1 < right:
                node.right = TreeNode()
                root_and_indexes.append((node.right, middle + 1, right))
        return root

```

## Step3

- step2 と同じコードで練習終りました。
- 今回も前回の問題と同じような書き方を選ぶかと思いましたが、自分の中にも何かこだわりのようなものがあるようですね。

```python

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        root = TreeNode()
        root_and_indexes = [(root, 0, len(nums))]
        while root_and_indexes:
            node, left, right = root_and_indexes.pop()
            middle = (left + right) // 2
            node.val = nums[middle]
            if left < middle:
                node.left = TreeNode()
                root_and_indexes.append((node.left, left, middle))
            if middle + 1 < right:
                node.right = TreeNode()
                root_and_indexes.append((node.right, middle + 1, right))
        return root

```

