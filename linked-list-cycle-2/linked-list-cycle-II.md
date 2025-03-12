## お題

- 連結リストの先頭を表すノードheadが与えられます。その連結リストにサイクルがあればその開始地点を返してください。サイクルがなければnullを返してください。
- 与えられた連結リストにノードが1つしかない場合は、サイクルがないものとします。

## 考えたこと

- 直感で、[141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)で使った考え方がほとんど使えそうだと思いました。
    - https://github.com/shintaro1993/arai60/pull/3/files

## Step1

- サイクルがある場合の判定に、過去に見つけたノードをメモしたものを利用する方法。visited_nodesにノードの重複が起きないことを保証する。
- 与えられた連結リストのノードの数をnとする
- 時間計算量: O(n)
- 空間計算量: O(n)

```Python

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited_nodes = set()
        node = head
        while node:
            if node in visited_nodes:
                return node
            visited_nodes.add(node)
            node = node.next
        return None

```

- ここまで10分かからないくらいでした。
- 他の選択肢も探してみよう。

## 調べたこと

- setの動作について
    - setの各種操作をするとき、対象とするオブジェクトに実装されているhash()関数を呼んでその値を利用しているらしい
        - 参考資料
            - [object.__hash__(self)](https://docs.python.org/3/reference/datamodel.html#object.__hash__)
    - setではlookup関数にOpen addressingが使われているらしい
        - [setobject.c](https://github.com/python/cpython/blob/1fb7e2aeb7e4312b7f20f0d5f39ddd00d7762004/Objects/setobject.c#L7)
            >    The basic lookup function used by all operations.This is based on Algorithm D from Knuth Vol. 3, Sec. 6.4.
        - [dictobject.c](https://github.com/python/cpython/blob/4dcbe06fd264b3f9c0b26831f19d211a48c52286/Objects/dictobject.c#L1230C1-L1233C67)
            > The basic lookup function used by all operations.
    This is based on Algorithm D from Knuth Vol. 3, Sec. 6.4.
    Open addressing is preferred over chaining since the link overhead for
    chaining would be substantial (100% with typical malloc overhead).
- set の `x in s` の計算量
    - average case: O(1)
    - worst case: O(n)
    - 参考資料
        - [Time Complexity](https://wiki.python.org/moin/TimeComplexity)

## Step2

- discord内やコメント集を調べてみました。

- https://github.com/5ky7/arai60/pull/3/files#diff-7d8fb928dfae99b0348d1c6a09f7cf44f7c09c1e0080cabab132c5042da353c3
    - while文の中で見つかった場合と見つからなかった場合の返却処理を済ませることは頭になかった。
- https://github.com/fuga-98/arai60/pull/2
    - 変数に複数の値が含まれることを明示させたければ、変数名を xxx_nodes としてもいいらしい
    - 償却計算量の話があった
        - [Time Complexity](https://wiki.python.org/moin/TimeComplexity)の資料を再度確認したら、setではOperationの横にAverage caseとWorst caseが並んでいるのに、dictの横にはAverage caseとAmortized Worst Caseが並んでいる。なぜ違うのか。
        - [Wikipedia: Amortized analysis](https://en.wikipedia.org/wiki/Amortized_analysis)に以下の記載があった。dictのOperationのworst-caseのrun timeはpessimisticだが、setにおいてはpessimisticだと考えられていないのかもしれないと思った。
            > The motivation for amortized analysis is that looking at the worst-case run time can be too pessimistic. 
        - setはdictionariesと違って、membership testで要素が見つかった場合と見つからなかった場合の両方を最適化しているため、worst-caseがpessimisticではないとの判断になり、Amortized Worst CaseではなくWorst caseでmembership testなどを見ているのかな。
            - [setobject.c](https://github.com/python/cpython/blob/1fb7e2aeb7e4312b7f20f0d5f39ddd00d7762004/Objects/setobject.c#L27)
                >    Use cases for sets differ considerably from dictionaries where looked-up
   keys are more likely to be present.  In contrast, sets are primarily
   about membership testing where the presence of an element is not known in
   advance.  Accordingly, the set implementation needs to optimize for both
   the found and not-found case.
- https://github.com/mura0086/arai60/pull/7
    - 以下の資料を参考に、うさぎとかめを使って整理してみる
    - [コメント集: 142. Linked List Cycle II](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.jfs03xpyyrfl)
        - 距離を記号などに置き換えずに、状況を自然な言葉だけを使って説明していて、こんなこともできるのだなと驚いた。

- サイクルがない場合の処理も忘れずに、コメント集にあった説明を自然な感覚でコードに置き換えてみる

```Python

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
                
        if fast is None or fast.next is None:
            return None

        slow = head
        while fast:
            if slow == fast:
                return fast
            slow = slow.next
            fast = fast.next

        return None

```

- https://github.com/tayzarnw/LeetCode/pull/4/files
    - サイクルが見つからなかった場合を`if fast is None or fast.next is None`で判定しているが、サイクルが見つかったときにその情報を変数に格納して処理をするのもわかりやすくなるなと思った。

- https://github.com/hayashi-ay/leetcode/pull/18/files#diff-97a2b5510d65cd5c736cab9a3675eb2122bfe5e9ccbe491032aad6fee9d3f74dR133
    - 自分の書いたコードだと、サイクルが存在しない場合がわかるのがwhileループに入った後になっているが、衝突点を探す処理を関数化してwhileループに入る前にサイクルが存在しない場合をreturnさせる方法もあるようで確かにそれもありだなと思った。

## Step3

- Step1のコードが、処理の流れを追いやすくて好みです。
- 3回とも一分以内で書けました。