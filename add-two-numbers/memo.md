# 2. Add Two Numbers

## Step1

- まずは動くコードを書く。
- 完成品の先頭と末尾を管理しながら、各桁の計算結果を完成品の末尾に追加していくことを考えました。

```python

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        tail = dummy_head
        carry = 0
        while l1 or l2:
            value_of_l1 =  0
            value_of_l2 =  0
            if l1:
                value_of_l1 = l1.val
            if l2:
                value_of_l2 = l2.val
            sum_digit = value_of_l1 + value_of_l2 + carry
            tail.next = ListNode(sum_digit % 10)
            tail = tail.next
            carry = sum_digit // 10
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        if carry:
            tail.next = ListNode(carry)

        return dummy_head.next

```

- n を二つの連結リストのそれぞれのノードの数の多い方の数とします。
- 時間計算量: O(n)
- 空間計算量: O(1)
- 時間は15分くらいかかりました。

## Step2

### 調べたこと

- https://discord.com/channels/1084280443945353267/1196472827457589338/1197166381146329208
    - 再帰を使った実装。帰りがけにも処理をすることにより、stack + loop に書き直すのが面倒になっている。これを避けるために dummy を使うことを考える。
    - dummy を使わない while + loop の実装における stack の中身は、以下をイメージしました。
        - stackの中身
            1. (行き、1)
            2. (帰り、1), (行き、2)
            3. (帰り、1), (帰り、2), (行き、3)
- https://discord.com/channels/1084280443945353267/1235829049511903273/1238532322991800350
    - 帰りがけの再帰を stack と while ループに置き換えている。while 文中の最初の処理は pop ではなく top であることに注意する。
- https://github.com/kazukiii/leetcode/pull/6#discussion_r1633605853
    - dummyを使わない実装の話。
- https://discord.com/channels/1084280443945353267/1195700948786491403/1197168055864791133
    - 変数を減らす方法として参考になりました。
        > if curr1:
        >   digit_sum += curr1.val
        > if curr2:
        >   digit_sum += curr2.val
- https://discord.com/channels/1084280443945353267/1334041281902547036/1337122579877728307
    - 番兵を使うことで桁の合計の計算をシンプルに行う方法もある。改めて自分が最初に思い付い方法以外にも選択肢があるということを実感した。
- https://github.com/fhiyo/leetcode/pull/5/commits/f2e20f4d25a90b2fd41c44fc33005a620646d0fd
    - ノードから値を取得するときやポインタを進めるときの処理を関数に切り出す発想が自分にはなかったので持っておこうと思いました。

- 自分の最初の感覚では `if carry:` がある方が自然な流れだと感じたが、それがあることによって読む人の助けになるか考えると、特に助けにはなっていないように思った。一番最初にやったことを自然だと感じる癖があるかもしれない。

```python

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        tail = dummy_head
        carry = 0
        while l1 or l2 or carry:
            sum_digit = carry
            if l1:
                sum_digit += l1.val
            if l2:
                sum_digit += l2.val
            tail.next = ListNode(sum_digit % 10)
            tail = tail.next
            carry = sum_digit // 10
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy_head.next

```

## Step3

- `sum_digit = carry`の後に二つ if 文を通るのが煩わしく感じ、修正しました。最初見たときは追加でノードを作ることに抵抗を感じましたが、そもそもダミーノードを使わない選択肢がある中でダミーノードを使う選択をしているので、特に強い理由がない中でこれに抵抗を感じすぎることもないのかなという気持ちに変わりました。よく見ると l1 と l2 を更新するときの条件も消すことができ、うれしい気持ちになりました。

```python

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode(None)
        tail = dummy_head
        carry = 0
        while l1 or l2 or carry != 0:
            if not l1:
                l1 = ListNode(0)
            if not l2:
                l2 = ListNode(0)

            sum_digit = l1.val + l2.val + carry
            tail.next = ListNode(sum_digit % 10)
            tail = tail.next
            carry = sum_digit // 10
            l1 = l1.next
            l2 = l2.next

        return dummy_head.next

```

- 5分以内に3回かけることを確認しました。
- sum_digit はもしかすると total の方が誤解がない気が少ししてきた。

## Step4

- 調べているときに見つけたほかの実装方法や書きかえ方の練習
- 書き換えが目的のため、コンパクトに書ける方法を選択したので改めて見直す

### dummy を使った再帰とそれを while + loop の形になおしたもの

- dummy を使った再帰

```python

class Solution:
    def helper(self, prev, l1, l2, carry):
        if not l1 and not l2 and carry == 0:
            return None
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        sum_digit = val1 + val2 + carry
        node = ListNode(sum_digit % 10)
        next_l1 = l1.next if l1 else None
        next_l2 = l2.next if l2 else None
        prev.next = node
        self.helper(node, next_l1, next_l2, sum_digit // 10)
        
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        self.helper(dummy_head, l1, l2, 0)
        return dummy_head.next

```

- 上記を while + loop の形になおしたもの

```python

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode()
        stack = [(dummy_head, l1, l2, 0)]
        while stack:
            prev, l1, l2, carry = stack.pop()
            if not l1 and not l2 and carry == 0:
                break
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            sum_digit = val1 + val2 + carry
            next_l1 = l1.next if l1 else None
            next_l2 = l2.next if l2 else None
            node = ListNode(sum_digit % 10)
            prev.next = node
            stack.append((prev.next, next_l1, next_l2, sum_digit // 10))
        
        return dummy_head.next

```

### dummy を使わない再帰とそれを while + loop の形になおしたもの

- dummyを使わない再帰

```python

class Solution:
    def helper(self, l1, l2, carry):
        if not l1 and not l2 and carry == 0:
            return None
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        sum_digit = val1 + val2 + carry
        node = ListNode(sum_digit % 10)
        next_l1 = l1.next if l1 else None
        next_l2 = l2.next if l2 else None
        node.next = self.helper(next_l1, next_l2, sum_digit // 10)
        return node

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        return self.helper(l1, l2, 0)
        
```

- 上記を while + loop の形に直したもの
- 行きがけの処理と帰りがけの処理を区別するために、backという変数を用意しました。stackの中身としては、backの値、l1、l2、carryの値、各桁の計算結果を格納するnodeとしています。
- `stack[-1][4]`の処理が分かりにくく感じるため、stack に保存するものを tupple 以外にすることも考えています。

```python

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        stack = [(False, l1, l2, 0, None)]
        while stack:
            back, l1, l2, carry, node = stack.pop()
            if back and not stack:
                result = node
                continue 
            if back:
                stack[-1][4].next = node
                continue

            if not l1 and not l2 and carry == 0:
                continue
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            sum_digit = val1 + val2 + carry
            node = ListNode(sum_digit % 10)
            next_l1 = l1.next if l1 else None
            next_l2 = l2.next if l2 else None
            stack.append((True, None, None, None, node))
            stack.append((False, next_l1, next_l2, sum_digit // 10, None))

        return result

```

dummy を使わない再帰と使う再帰の違いについて、再帰だけを見てると dummy を使わない方がコンパクトでよさそうに感じたが、while + loop に書き換えることを考えると実装の重さが意外と違っていて驚いた。できるだけ多くの選択肢を理解したいと思うが、一方で時間が意外とかかるため、一時撤退するタイミングもつかんでいきたい。

## 全体を通しての感想

- 他の方の書いたコードを読んだり考え方の違いを発見することで、そもそも選択肢を一つ見つけて満足するだけでは、やるべきことをやりましたとは言えないなという気持ちになった。