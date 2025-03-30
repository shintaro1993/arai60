# 82. Remove Duplicates from Sorted List II

## Step1

- 紙に絵を書いて考えてみました。完成品の最後のノードを指す変数としてpreviousを用意して、値が重複しているグループを見つけたらそれらを削除するイメージを思い浮かべました。


```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        previous = dummy
        current = head
        while current:
            if current.next and current.val == current.next.val:
                while current.next and current.val == current.next.val:
                    current = current.next
                previous.next = current.next
            else:
                previous = previous.next
            current = current.next
        return dummy.next

```

- if文の中にwhile文があって、ネストが深くなっていることが気になりました。
- どのように考えればいいかdiscord内を調べてみます。

## 調べたこと

- https://discord.com/channels/1084280443945353267/1195700948786491403/1197102971977211966
    - 一番最初に書かれたコードは同じ処理が複数の個所に存在しており、第一印象としてこういうことをやってもいいのかと思った。しかしこれは自然言語を素直に直しているように思えて、逆に自分が最初の一歩目で完成形のコードを作らないといけないと思いすぎていたと思えてきた。
- https://github.com/t0hsumi/leetcode/pull/4#discussion_r1856455749
    - 「切断しておいて繋ぐ」、「繋いでおいて切断」などの話題がある。どういう状態を約束するか考えられなかった。また自分としては作業場所と完成品の場所を分離させておいた方が作業がやりやすいなと思った。
- https://discord.com/channels/1084280443945353267/1262761766887358557/1324487325077475348
    - 自分のコードでpreviousと名前がついていて動かないものを、他の人はそれに注目してループで動かすという発想があることは考えられなかった。
- https://github.com/yus-yus/leetcode/pull/4#discussion_r1939063888
    - dummyノードを使わずに後で実装してみよう
- https://github.com/SanakoMeine/leetcode/pull/5#discussion_r1904136390
    - node.nextとnode.next.nextを使ったコードが提示されている。自分の中で選択肢として見えておらず、また見た後も選択しないように感じる選択肢が、常識の範囲の中に含まれていることを認識した。
- https://github.com/colorbox/leetcode/pull/20#discussion_r1667689672
    - 自分の中でもcurrentを使いたい明確な理由が出せなかったので、変数名はnodeにしようと思う。
- https://discord.com/channels/1084280443945353267/1183683738635346001/1183691370683174973
- https://discord.com/channels/1084280443945353267/1226508154833993788/1249911168265355285
    - 自分はこの問題をlinked list特有の問題だと認識していたので、vectorでの実装やgroupby・filter・concatとの関連性が最初わからなかった。データ構造の差を取り除いて考える視点は、今何をやっているのか理解をする助けになるなと思った。

## Step2

### 実装1

- 調べた内容を参考にして、実装1と実装2を、「重複を見つけたら帰らずに削除してから帰る」という発想で、ダミーノードを使って実装してみました。完成品の最後の次がNoneであることを保証しているものと、ダミーノードを入力リストの先頭に差し込んだもので書いてみました。完成品に含めるものの最後の次をNoneにするだけで、頭の中での状況の見え方が結構変わる。完成品置き場と作業場所を分けた方が作業に集中できてわかりやすく感じました。

```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(None, head)
        last_of_unique = dummy
        node = head
        while node:
            if not node.next or node.val != node.next.val:
                last_of_unique = node
                node = node.next
                continue
            duplicate_value = node.val
            while node and node.val == duplicate_value:
                node = node.next
            last_of_unique.next = node
        return dummy.next

```

### 実装2

```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(None)
        last_of_unique = dummy
        node = head
        while node:
            if not node.next or node.val != node.next.val:
                last_of_unique.next = node
                node = node.next
                last_of_unique = last_of_unique.next
                last_of_unique.next = None
                continue
            duplicate_value = node.val
            while node and node.val == duplicate_value:
                node = node.next
        return dummy.next

```

### 実装3

- ダミーノードを使わずに書いてみました。whileループに入る前に初期値をずらすことを考えましたが、自分の中での書き換えのしやすさという点でこのように書いてみました。完成品の置き場と作業場所を分けているので変更しやすく感じました。

```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        result = None
        last_of_unique = None
        node = head
        while node:
            if not node.next or node.val != node.next.val:
                if result is None:
                    result = node
                if last_of_unique:
                    last_of_unique.next = node

                last_of_unique = node
                node = node.next
                last_of_unique.next = None
                continue
            
            duplicate_value = node.val
            while node and node.val == duplicate_value:
                node = node.next
        
        return result

```

### 実装4

- 完成品の最後に追加できるものを見つけてそれを追加するという考え方で書いてみました。

```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode(None)
        last_of_unique = dummy_head
        node = head
        while node:
            candidate = node
            while node and node.val == candidate.val:
                node = node.next
            if candidate.next == node:
                last_of_unique.next = candidate
                last_of_unique = last_of_unique.next
                last_of_unique.next = None
        return dummy_head.next
```

- 実装4の修正
    - deleteDuplicatesという関数の中に、candidateという名前だけだと削除する候補なのかとっておく候補なのかわかりづらいと思ったので、変数名をcandidate_to_storeにしました。storeをわかりづらく感じたら教えていただけますと幸いです。
    - if文は条件をひっくり返して、下の処理のネストを浅くしました。

```python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_head = ListNode(None)
        last_of_unique = dummy_head
        node = head
        while node:
            candidate_to_store = node
            while node and node.val == candidate_to_store.val:
                node = node.next
            if candidate_to_store.next != node:
                continue
            candidate_to_store.next = None
            last_of_unique.next = candidate_to_store
            last_of_unique = last_of_unique.next
        return dummy_head.next

```

## Step3

自分の中では実装4を修正したものが少しわかりやすく感じたのでこれを何度もかけるように練習しました。ダミーノードを使わずに書いたりするなど、複数の実装を試すことで、変数など、それが何なのかを考えるきっかけになってよい練習だと思いました。