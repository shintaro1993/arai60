# 206. Reverse Linked List

## Step1

- 考えたこと
    - 方法1：入力で受け取った連結リストのノードを先頭から一つずつ、返却用のリストの先頭に追加していく
    - 方法2：受け取った連結リストの先頭からすべてのノードを、 stack に保存し、取り出しながら返却用のリストの末尾に追加していく

- 時間計算量：O(n)
- 空間計算量：O(1)

### 方法1

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        reversed_head = None
        node = head
        while node is not None:
            next_node = node.next
            node.next = reversed_head
            reversed_head = node
            node = next_node
        return reversed_head

```

- 時間計算量：O(n)
- 空間計算量：O(n)

### 方法2

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        stack = []
        while node is not None:
            next_node = node.next
            node.next = None
            stack.append(node)
            node = next_node

        dummy_head = ListNode()
        tail = dummy_head
        while stack:
            node = stack.pop()
            tail.next = node
            tail = tail.next
        
        return dummy_head.next

```

ここまで15分くらいかかりました。

## Step2

### 調べたこと

- https://discord.com/channels/1084280443945353267/1231966485610758196/1239417493211320382
    - 再帰のコードを書いていなかったので、自分も後で書こう
- https://github.com/irohafternoon/LeetCode/pull/9/files
    - stack を使う方法で、一つだけ stack に入れないようにしていたのは自分にはない考えだった。ただ、コメントがあったのでコードを読むときに助けられた。自分もコードの中にコメントを入れる必要があるかどうかをもっと考えるようにしていこうと思う。
- https://github.com/TORUS0818/leetcode/pull/9/files#r1598051541
    - 自分が step1 の一つ目で書いたようなコードで、今のやり方では node 変数の意味が reversed と混ざってしまっているという話がある。自分は意味が混ざるということにあまり抵抗を持っていない気がするので、咀嚼するのにもう少し時間を使いたい。

### 再帰で実装をする。

- 考えたことは、行きがけで繋ぎ変える方法と、帰りがけで繋ぎ変える方法

- 行きがけで繋ぎ変える方法

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.reverse_list_helper(None, head)

    def reverse_list_helper(self, prev, node):
        if node is None:
            return prev
        next_node = node.next
        node.next = prev
        prev = node
        return self.reverse_list_helper(prev, next_node)

```

- 帰りがけで繋ぎ変える方法

```python 

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        head, _ = self.reverse_list_helper(head)
        return head

    def reverse_list_helper(self, node):
        if node is None or node.next is None:
            return node, node

        next_node = node.next
        node.next = None
        head, tail = self.reverse_list_helper(next_node)
        tail.next = node
        return head, node

```

- ダミーノードを使うことでstep1で書いたコードを少し変形した形になったが、読みやすさはあまり変わっていないように思う。改めて復習するときに見比べてどう思うか調べてみよう。

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        node = head
        while node is not None:
            next_node = node.next
            node.next = dummy_head.next
            dummy_head.next = node
            node = next_node
        return dummy_head.next

```

## Step3

- こちらでコードを書く練習をしました。

```python

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        reversed_head = None
        node = head
        while node is not None:
            next_node = node.next
            node.next = reversed_head
            reversed_head = node
            node = next_node
        return reversed_head

```

##  感想

- 調べたときに見つけた以下の議論について考えていました。そこで話題にあった指摘に対して、レビュワーの方と同じ温度感で「嫌だな」という気持ちを共有できていると感じておらず、もしこれが仕事だった場合にどうすればいいのかなと考えてしまいました。できることとしては、その人の言っていることを理解できるように努めることと、代替の案を提示することでしょうか。レビューの場で自分にできることについてもこれから考えて行きたいなと思いました。

> - https://github.com/TORUS0818/leetcode/pull/9/files#r1598051541
>    - 自分が step1 の一つ目で書いたようなコードで、今のやり方では node 変数の意味が reversed と混ざってしまっているという話がある。自分は意味が混ざるということにあまり抵抗を持っていない気がするので、咀嚼するのにもう少し時間を使いたい。