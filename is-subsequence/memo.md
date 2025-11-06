# Is Subsequence

## step1

二つの文字列 s と t が与えられるs。s が t の subsequence かどうか判断する。

テストケース:
- t = "abcde",      s = "ace"  -> True
- t = "abcde",      s = "acb"  -> False
- t = "abcde",      s = ""     -> True
- t = "",           s = "abc"  -> False
- t = "",           s = ""     -> True 

制約:
- 0 <= s.length <= 100
- 0 <= t.length <= 10^4
- s と t は lowercase English letters のみで構成される

s においてまだ t とマッチしていない部分の先頭のインデックスを管理する。p = 0 で初期化し、 [p:len(s)) がこれから調べる領域。t でループを回しながら t[q] == s[p] なら p をインクリメントし、そうでないなら何もせず次のループに進む。ループが終了したとき p == len(s) になっていれば、 s における t とマッチしていない部分がなくなったので、s が t の subsequence だとする。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        match_length = 0
        for i in range(len(t)):
            if match_length == len(s):
                return True
            if t[i] != s[match_length]:
                continue
            match_length += 1
        return match_length == len(s)

```

最初は return True のところを break にしていたけど、True の方が少し自然な気がする。t[len(t) - 1] でマッチしたときのことを考えると、最後に match_length == len(s) が必要だし、s[match_length] する前にインデックスのチェックをする必要があるし厄介。もう少し整理できないかと思う。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        
        match_length = 0
        for i in range(len(t)):
            if t[i] != s[match_length]:
                continue
            match_length += 1
            if match_length == len(s):
                return True
        return False

```

match_length はもっとシンプルでもいいかもしれない。

n = len(t)
時間計算量: O(n)
- だいたい0.01秒の時間で考えておく
空間計算量: O(1)

Follow up:
Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?

現状ループを t で回しているが、たくさんの s に対して判定を行いたい場合は s でループを回せるとうれしいよね、みたいな気持ちかな。
t の文字をキーにしてインデックスのリストを対応させれば、s でループを回しながら二分探索でいけそうかな。

以下のコードだと同じ関数で 辞書を作っているので 時間計算量は O(n + mlogn) くらいで考える。空間計算量は O(n) 。複数の s をリストなどで受け取ったりする場合は選択肢としてはありかもしれない。

```python

import bisect
from collections import defaultdict


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        letter_to_indices = defaultdict(list)
        for i, letter in enumerate(t):
            letter_to_indices[letter].append(i)

        last_matched_index = -1
        for letter in s:
            if letter not in letter_to_indices:
                return False
            
            letter_indices = letter_to_indices[letter]
            index = bisect.bisect_right(
                letter_indices,
                last_matched_index,
            )
            if index == len(letter_indices):
                return False
            last_matched_index = letter_indices[index]
        return True

```

## step2

- https://discord.com/channels/1084280443945353267/1201211204547383386/1231637671831408821
    - 正規表現のエスケープの話はもう少し調べてみよう

- https://discord.com/channels/1084280443945353267/1225849404037009609/1243290893671465080
    - while を使う方法もあるし、書き換え方もいろいろある。どれが自然かはまだ何とも言えない気がするので広い気持ちを持っておこう。

- https://github.com/Yoshiki-Iwasa/Arai60/pull/62/files
    - 無限ループについての感覚。
        > 無限ループはそこそこよく使います。
        > それはそうと、一回頭の中でそういうのを経由すると変形の範囲が広がるので、仮にそれを使いたくなかったとしても視野にはいれておくといいと思いますね。
    - 動的計画法など、思っているよりもいろいろな考えがある。
    - s_index, t_index で読みやすいかもしれない。s_c, t_c は難しいかもしれない。

- https://github.com/olsen-blue/Arai60/pull/58/files
    - 変数名は s_index, t_index の方が共通の認識としてよさそうか。
    - find にこういう使い方があったのか
        - https://docs.python.org/3/library/stdtypes.html#str.find

- https://github.com/ryosuketc/leetcode_arai60/pull/57/files

無限ループから考えるのはいいかもしれない。
return True と return False の順番に注意。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_index = 0
        t_index = 0
        while True:
            if s_index == len(s):
                return True
            if t_index == len(t):
                return False
            
            if s[s_index] != t[t_index]:
                t_index += 1
                continue
            s_index += 1
            t_index += 1

```

s[s_index] に対して、マッチする t[t_index] が見つかるまで探し続ける。
while s_index < len(s) が個人的に好きかも。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_index = 0
        t_index = 0
        while s_index < len(s):
            if t_index == len(t):
                return False
            
            if s[s_index] == t[t_index]:
                s_index += 1
            t_index += 1
        return True

```

t に注目するなら step1 の変数名を変えたものもいいかな。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        
        s_index = 0
        for t_index in range(len(t)):
            if t[t_index] != s[s_index]:
                continue
            s_index += 1
            if s_index == len(s):
                return True
        return False

```

## step3

こちらの形で練習しました。

```python

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_index = 0
        t_index = 0
        while s_index < len(s):
            if t_index == len(t):
                return False
            
            if s[s_index] == t[t_index]:
                s_index += 1
            t_index += 1
        return True

```