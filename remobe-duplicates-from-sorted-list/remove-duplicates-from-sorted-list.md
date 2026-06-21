## お題

- 整数を値に持つ連結リストが昇順でソートされた状態で与えられます。ソートされた状態を保ったままで、かつすべての重複が削除された状態にして、連結リストを返してください。

## 考えたこと

- duplicatesとは
    - あるものが存在していてそのコピーが作られたとき、そのコピーのことをduplicateと呼ぶという理解。今回はduplicateが複数存在しているということ。
    - https://dictionary.cambridge.org/dictionary/english/duplicate?q=duplicates+
        > noun: something that is an exact copy of something else:

## 作業内容

- 与えられた連結リストは昇順で並んでいるので、ノードが持つ値ごとにグループに分けて考える。各グループの左端のノードをoriginalとして、それ以外をduplicateとする。originalがある場所にaさんに立ってもらい、bさんには右に一つずつノードを見ていってもらう。bさんは、次のグループのoriginalを発見したらaさんに報告してoriginalの次を今回発見したoriginalに繋ぎ変えてもらい、次はここに移動してきてもらう。この作業をすべてのノードを調べ終わるまで続けてもらう。
- aさんは初期値としてoriginalがある場所に立っている。aさんの仕事は今いるoriginalを次のoriginalに繋ぎ変えて次のoriginalに移動すること。bさんの仕事は次のoriginalを見つけてaさんに報告すること。全体としてheadから各グループのoriginalを順にたどれることを保証する。


## Step1

- 連結リストのすべてのノードの数をnとする。
- 時間計算量：O(n)
- 空間計算量：O(1)

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
            
        original = head
        node = head
        while node:
            if original.val != node.val:
                original.next = node
                original = node
            node = node.next

        original.next = None
        return head

```

- ここまで20分くらいかかった。状況に対する認識を言語化することに時間がかかっている。日常の中で認識を言語化する練習をしていこうと思う。
- whileループを出た後に仕事が残っているので忘れないようにしないといけない。この処理をループの中でできないか考えよう。

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:            
        if head is None:
            return None
            
        original = head
        node = head
        while True:
            if node is None:
                original.next = None
                return head
            if original.val != node.val:
                original.next = node
                original = node
            node = node.next

        return head

```

- わかりにくくなった気がする
- headがNoneかどうかのチェックをなくす方法も考える

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        original = head
        node = head
        while node:
            if original.val != node.val:
                original.next = node
                original = node
            node = node.next

        if original:
            original.next = None
        return head

```

- headがNoneの場合に下の方まで処理を進めてもいいのかという気持ちがある。
- headがNoneの場合は`original.next = None`でエラーになるのでこの位置で判定するか、先頭で切り分けるのがいいかな。
- ダミーノードを先頭に差し込むとheadがNoneの場合を特別に考えなくてもすみそう

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:            
        dummy = ListNode(None, head)
        original = dummy
        node = dummy
        while node:
            if original.val != node.val:
                original.next = node
                original = node
            node = node.next

        original.next = None
        return head

```

- 少しやりすぎな気はするかな
- `original.next = None`をどうにかできないか。

## Step2

- https://github.com/myzn0806/leetcode-2/pull/3/files
    - ループの各ステップで重複を発見したときに繋ぎ変えを行う方法もある。行数を減らせる。
    - 重複を見つけた場合をcontinueにする方法もある。
- https://github.com/fuga-98/arai60/pull/4/files
- https://github.com/yus-yus/leetcode/pull/3/files
    - ループで使う変数を一つにする方法もある。
    - 考え方の違いでコードの見た目が結構変わっている。そもそもの考え方を複数持った方がよさそうかな。
- https://github.com/hayashi-ay/leetcode/pull/20/files
    - `prev_node.next = None`があった。
- [コメント集: Remove Duplicates from Sorted List](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0)
    - 南京錠を使ったたとえ話がしっくり来た。自分は、二人で一日で作業をしようと考えていた気がする。引継ぎ資料を作って、複数人で分担する視点を持って書いてみよう。


```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:          
        unique_tail = head
        node = head
        while node:
            if unique_tail.val == node.val:
                unique_tail.next = node.next
            else:
                unique_tail = node
            node = node.next
        return head

```

- uniqeu_tailが作業済みの末尾、nodeが未処理の先頭で考えているので、初期値が同じになっていることに少し違和感がある。

## Step3

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:          
        if not head:
            return head
        unique_tail = head
        node = head.next
        while node:
            if unique_tail.val == node.val:
                unique_tail.next = node.next
            else:
                unique_tail = node
            node = node.next
        return head

```

- nodeだけで処理するのもシンプルでいいかも

```Python

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        while node and node.next:
            if node.val == node.next.val:
                node.next = node.next.next
                continue
            node = node.next
        return head

```

- 