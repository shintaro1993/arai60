# yield from について整理したこと。

- https://discord.com/channels/1084280443945353267/1192736784354918470/1235116690661179465
    - 再帰 + yield + yield from での実装
    - yield from について
        - https://docs.python.org/3/reference/expressions.html#generator-expressions
            > A generator expression is a compact generator notation in parentheses: ... A generator expression yields a new generator object.
        - https://docs.python.org/3/reference/expressions.html#yield-expressions
            > The yield expression is used when defining a generator function or an asynchronous generator function and thus can only be used in the body of a function definition. Using a yield expression in a function’s body causes that function to be a generator function
            > When yield from <expr> is used, the supplied expression must be an iterable.
        - https://docs.python.org/3/whatsnew/3.3.html#pep-380
            > For simple iterators, yield from iterable is essentially just a shortened form of for item in iterable: yield item:
        - https://peps.python.org/pep-0380/
        - https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-yield-from-syntax-in-python-3-3

- yield の基本動作の確認

```python

def g():
    yield 1
    yield 2
    yield 3

for num in g():
    print(num)

```

- inorder_sort では、再帰的にこういう感じのことが起きているのかな。

```python

def h():
    for n in range(1, 6):
        yield n

def i():
    for n in range(7, 11):
        yield n

def g():
    yield from h()
    yield 6
    yield from i()

for n in g():
    print(n)

```

- 再帰ではないですけれど、こんなことができるみたいですね。

```python

def i():
    for n in range(1, 6):
        yield n

def h():
    yield from i()
    for n in range(6, 11):
        yield n

def g():
    yield from h()

for n in g():
    print(n)

```

- 少し動きが分かったような気がするけど、実際使えるかは怪しいな。

```python

import math


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def yield_inorder_nodes(node):
            if node is None:
                return 
            if node.left is not None:
                yield from yield_inorder_nodes(node.left)
            yield node
            if node.right is not None:
                yield from yield_inorder_nodes(node.right)

        previous_value = -math.inf
        for node in yield_inorder_nodes(root):
            if node.val <= previous_value:
                return False
            previous_value = node.val
        return True
        
```

- yield from yield_inorder_nodes() はどうかと思ったけど、関数名に yield をつけるのはありなのかな。
    - https://source.chromium.org/search?q=lang:python%20yield&start=31