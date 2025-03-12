## お題

連結リストの先頭を表す変数headが与えられます。その連結リストにサイクルが存在するか調べてください。
連結リストの先頭からnextをたどって探索していったときに、すでに見つけたことのあるノードが再度見つかった場合、連結リストにサイクルが存在するといいます。サイクルが見つかった場合trueを、見つからなかった場合falseを返してください。

## 考えたこと

- 今回考える連結リストはsingly linked listでよさそう
- Linked list
https://en.wikipedia.org/wiki/Linked_list
    - 連結リストにサイクルがあるということと、Circular linked listであるということは別物みたい

- サイクルが存在しない場合とは
    - すべての連結リストのノードを調べてもサイクルを発見できなかった場合サイクルが存在しなかったと報告してもよさそう。サイクルを発見した場合そこでreturnしたりして存在しない場合と合流しないように注意する。

- あるノードが過去発見済みかどうか調べる方法
    - これまでの作業で見つけたノードをメモしておく。各作業において今回の作業で見つけたノードがメモされているか調べる。過去にメモされていればサイクルを報告して作業終了。メモされていなければメモをして作業継続。

- 与えられた連結リストの先頭からノードを順にみていき、過去に発見済みのノードを再度見つけた場合はそこでサイクルが存在していることを報告して作業終了。連結リストのすべてのノードを調べてもサイクルが見つからなかった場合、サイクルがなかったことを報告して作業終了。

- 計算量

    - 与えられた連結リストのノードの数をnとする

    - 時間計算量 
        - O(n): サイクルが見つかる場合も見つからない場合すべてのノードを調べるため。

    - 空間計算量
        - O(n): サイクルが見つかる場合もサイクルが見つからない場合すべてのノードがメモに保存されるため。

## Step1

```Python

class Solution:
    def hasCycle(self, head):
        detected_nodes = set()
        node = head
        while node:
            if node in detected_nodes:
                return True
            detected_nodes.add(node)
            node = node.next
        return False

```

- 過去調べたノードのメモ用にdetected_nodesがよさそうと思ったけど、この言葉を使うとなんだか大げさなことをやる印象を与えそうだなと思った。他に良いものがないか探す。

    - https://dictionary.cambridge.org/dictionary/english/detect?q=detected
    > to notice something that is partly hidden or not clear, or to discover something, especially using a special method:

- ここまで20分くらいかかった。

## Step2

- 他の方のコードを調べたりコメント集を確認する

- https://discord.com/channels/1084280443945353267/1195700948786491403/1195944696665604156
    - 自然な方法を意識していると、フロイドのうさぎとかめは思いつけなかった。
- https://github.com/cheeseNA/leetcode/pull/6/files
    - setのハッシュ関数がどうなっているのかまで疑問に思わなかった。問題を解くことをゴールにしないよう注意しよう。
- https://github.com/momeemt/LeetCode/pull/1
    > 時間計算量から、おおよその実行時間を推測するやり方は分かりますでしょうか？
    - 実行時間まで考えられていなかった。
    - 再帰の考えはなかった。
- https://discord.com/channels/1084280443945353267/1183683738635346001/1204276545577943051
    > あ、なるほど、計算量という概念を知っているならば、あとは、1ループで何クロックか(何秒か)を考えて、具体的な n における秒数を計算するだけです。何クロックかについては、かなり難しいのですが、ここらへんを見ておくと10倍くらいの誤差で済むでしょう。
    - 後で計算してみよう

- フロイドのアルゴリズムの人多いな。

- https://github.com/TORUS0818/leetcode/blob/TORUS0818-patch-1/easy/141/answer.md
    - 見つけたノードをメモするデータにfoundとつけられていた。シンプル。
- https://github.com/nittoco/leetcode/pull/12/files
    - visited_nodeという変数名もあった。個人的に好みだけどnodesの複数形でない理由は何だろう。

```Python

class Solution:
    def hasCycle(self, head):
        visited_nodes = set()
        node = head
        while node:
            if node in visited_nodes:
                return True
            visited_nodes.add(node)
            node = node.next
        return False

```
- 2分くらいで何度でもかけると思う。

- フロイドも書いてみよう

## Step3

- フロイド版
    - これは一つずつ進むポインタ(slow)と2つずつ進むポインタ(fast)を用意して、二つのポインタがサイクルに入った後いずれぶつかるということを根拠にしているよう。
    - サイクルの中の辺の数をMとして、適当な二つのノードにslowとfastを置く。slowからfastまで時計回りにつながっているパスに含まれる辺の数をkとして、slowからfastまで半時計回りにつながっているパスに含まれる辺の数をM-kとする。ループ一つ進むことにより、後者の辺の数が1減っている。M-k回ループを回すことでslowとfastの間の辺の数が0になる。このことからループを回していけばいずれぶつかることが保証されていると考えていいのかな。
- 時間計算量: サイクルがある場合、slowポインタがサイクルに入ってからM-kステップでぶつかると思うので、O(n)
- 空間計算量: ポインタ二つ分なのでO(1)
```Python

class Solution:
    def hasCycle(self, head):
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

```
- 素直に書いたらこうなった。if文の位置が気になる。if文の位置をループ内の先頭に持ってくるためには、slowとfastの初期位置をずらさないといけない。でもそうするとfastの初期化でfast = head.nextとする前にhead.nextが存在するか確認しないといけないと思う。

```Python

class Solution:
    def hasCycle(self, head):
        if head is None or head.next is None:
            return False
        slow = head
        fast = head.next
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        return False

```
