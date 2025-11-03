# 920 · Meeting Rooms

## step1

ミーティングの開始時刻と終了時刻の組のリストが与えられる。すべてのミーティングに参加することができるか判定する。
[(0, 1), (1, 2)] の場合はどちらにも参加できる。

開始時刻を基準にしてソートし、ある会議の開始時刻が一つ前の会議の終了時刻と衝突していないかどうか調べて衝突が起きなかったらすべての会議に出席できると思う。

```python

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def can_attend_meetings(self, intervals: List[Interval]) -> bool:
        last_end_time = 0
        for interval in sorted(intervals, key=lambda interval: interval.start):
            if interval.start < last_end_time:
                return False
            last_end_time = interval.end
        return True

```

制約: 0 <= intervals.length <= 10^4
時間計算量: O(nlogn)
- Python で1秒間に100万ステップ処理できるとするとだいたい0.3秒くらいで考えておく
空間計算量: O(n)
要件として入力のリストが空の場合は True を返す。

- https://docs.python.org/3/library/functions.html#sorted

## step2

- https://github.com/Mike0121/LeetCode/pull/27/files
    - heap を使う方法もある。確かにそうだ。
    - Interval クラスに __lt__ が定義されていないので `TypeError: '<' not supported between instances` がでる。
        - https://docs.python.org/3/library/heapq.html
        - https://github.com/python/cpython/blob/1b376b82ac98517a55f13b5ec8645dc667762912/Lib/heapq.py#L283
    
- https://github.com/Yoshiki-Iwasa/Arai60/pull/60/files
    - this_end <= next_start のように一つ先を見るのもいいかも。
    - 条件式の並びを、`前回の end > 今回の start` にするのもいいと思うけど、数直線のイメージだと `今回の start < 前回の end` な気がしていて悩む。

- https://github.com/olsen-blue/Arai60/pull/56/files
    - 累積和を使う方法もあるんですね、なるほど。そこから座標圧縮をしたり。あとで整理しておこう。
    - for start, end in sorted(...) のように書きたいと思ったが、このクラスには __iter__ が定義されていなかったので他の書き方にしよう。
        - https://docs.python.org/3/library/stdtypes.html#iterator.__iter__
    > いや、Python は逆ですね。Perl は、「色々な方法がある」なのに対して、Python は「一つ、(そして、できれば一つだけ)理解しやすいやり方がある」ですね。
        - https://peps.python.org/pep-0020/
        - https://en.wikipedia.org/wiki/Perl#Philosophy
    - lambda では x がいいのかな。HOWTOs 見たら student だったので interval にしましたが。
        - https://docs.python.org/3/howto/sorting.html#key-functions

step1 を少し修正してみる

```python

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def can_attend_meetings(self, intervals: List[Interval]) -> bool:
        sorted_intervals = sorted(intervals, key=lambda x: x.start)
        last_end_time = 0
        for interval in sorted_intervals:
            if last_end_time > interval.start:
                return False
            last_end_time = interval.end
        return True

```

ソートしたものは変数に置かない方が読みやすい気がする。
interval.end なので last_end にした方が合ってるかな。

## step3

この形で練習しました。

```python

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def can_attend_meetings(self, intervals: List[Interval]) -> bool:
        last_end = 0
        for interval in sorted(intervals, key=lambda x: x.start):
            if last_end > interval.start:
                return False
            last_end = interval.end
        return True

```
