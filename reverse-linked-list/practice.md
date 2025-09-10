- 以下のレビューコメントをもとに Step2 で実装した、行きがけと帰りがけの再帰を while ループを使った実装になおしてみました。
    - https://github.com/shintaro1993/arai60/pull/11/files#r2045048653


## 行きがけの処理をなおしたもの

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        node = head
        while True:
            if node is None:
                break
            next_node = node.next
            node.next = prev
            prev = node
            node = node_next
        return prev

```

- 再帰のときは prev という変数名に違和感があまりなかったが、while になおすと違和感を感じたので変更しました。

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        reversed_head = None
        node = head
        while True:
            if node is None:
                break
            next_node = node.next
            node.next = reversed_head
            reversed_head = node
            node = node_next
        return reversed_head

```

## 帰りがけの処理をなおしたもの

- 帰りがけにも処理があるため `while True:` で書く方法がわからず、stack を使いました。`Add two numbers` の問題のときと違って帰りがけに処理をするために使う reversed_tail の管理が楽になっているなと感じました。

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        reversed_head = None
        reversed_tail = None
        stack = [(False, head)]
        while stack:
            back, node = stack.pop()
            if not back and (node is None or node.next is None):
                reversed_head = node
                reversed_tail = node
                continue
            
            # 行きの場合        
            if not back:
                next_node = node.next
                node.next = None
                stack.append((True, node))
                stack.append((False, next_node))
                continue

            # 帰りの場合
            reversed_tail.next = node
            reversed_tail = node

        return reversed_head

```