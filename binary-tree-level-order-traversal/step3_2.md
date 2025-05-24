- 内法表記のところを修正しました。

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
            nodes = [node for node in next_level_nodes if node is not None]
        return level_ordered_values

```

- 上のコードの修正をしたときに、こちらもいいかなと思い始めたので、こちらも練習しておく。

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