# 919 · Meeting Rooms II

## step1

すべての会議を行うために必要な最小の会議室の数を求める。

確保した会議室が0の状態からはじめて、会議の開始時刻と終了時刻が判明するごとに追加で会議室を確保する必要があるかどうか判断できればよさそうだと思った。
ソートしておいて会議の終了時刻を都度メモしていけば、継続中の会議で、前回の会議が始まってから今回の会議が始まるまでに終了した会議を特定することができる。(1, 2), (2, 3) は一つの会議室で問題ない。

```python

import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        num_required_rooms = 0
        num_using_rooms = 0
        end_times = []
        for interval in sorted(intervals, key=lambda x: x.start):
            while end_times and end_times[0] <= interval.start:
                heapq.heappop(end_times)
                num_using_rooms -= 1
            
            if num_required_rooms - num_using_rooms == 0:
                num_required_rooms += 1
            num_using_rooms += 1
            heapq.heappush(end_times, interval.end)
        return num_required_rooms

```

len(end_times) を使えば num_using_rooms は消せるしわかりやすくなりそう。

```python

import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        num_required_rooms = 0
        using_end_times = []
        for interval in sorted(intervals, key=lambda x: x.start):
            while using_end_times and using_end_times[0] <= interval.start:
                heapq.heappop(using_end_times)
            
            if num_required_rooms - len(using_end_times) == 0:
                num_required_rooms += 1
            heapq.heappush(using_end_times, interval.end)
        return num_required_rooms

```

時間計算量: O(nlogn)
- n <= 10^4 だとすると、だいたい0.3秒くらいで考えておく
空間計算量: O(n)

## step2

- https://github.com/nittoco/leetcode/pull/45/files
    - heap を使うにもいろいろな書き方がある。step1 はヒープを使っているけど meeting rooms の累積和を使った考え方のようなもののような印象がある。
    - step2 のコードは似てるなと思ったけど、max を使っているのは、一番重なっているところが気になるっていう感じかな。
    - len(ended_and_using) を使っているのは、最後の会議が始まった後も残っている会議室の数を使っているのかな。基本的に使い終わった会議室は返却せず使いまわせるときは使いまわすという感じかな。それもいいか。
        - 各部屋に対して、最終使用時刻を書き換えながら管理していくと考えるのがいいかも
        - https://github.com/skypenguins/coding-practice/pull/26/files#r2386264669

- https://github.com/olsen-blue/Arai60/pull/57/files
    - 解法3は nittoco さんの step1 を、ソートを使って累積和の考えで書いているのかな。もう少し考えたい。
    - prefix_sum は num_active_rooms くらいでもいいのかなという気がする。

- https://github.com/Yoshiki-Iwasa/Arai60/pull/61/files
    - 関数型的なものも勉強していこう。

heappop するところは continue でもいいかと思ったが、時刻を更新しないといけないのでこの形が自然になるかなあ。

```python

import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        used_end_times = []
        for interval in sorted(intervals, key=lambda x: x.start):
            if used_end_times and used_end_times[0] <= interval.start:
                heapq.heappop(used_end_times)
            heapq.heappush(used_end_times, interval.end)
        return len(used_end_times)

```

start と end をまとめてソートして、使っている会議室を管理していく方法。
タプルに 1 と -1 を使っているので、ソートしたときに意図している通りになるか注意する
    - https://github.com/Mike0121/LeetCode/pull/28/files#r1633611163

```python

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        timeline = []
        for interval in intervals:
            timeline.append((interval.start, 1))
            timeline.append((interval.end, -1))
        timeline.sort()

        num_required_rooms = 0
        num_active_rooms = 0
        for _, delta in timeline:
            num_active_rooms += delta
            num_required_rooms = max(num_required_rooms, num_active_rooms)
        return num_required_rooms

```

step1 の改善をする。`if num_required_rooms - len(using_end_times) == 0: ` は `if len(using_end_times) == num_required_rooms:` の方が分かりやすい気がしてきたので変更。

```python

import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        num_required_rooms = 0
        using_end_times = []
        for interval in sorted(intervals, key=lambda x: x.start):
            while using_end_times and using_end_times[0] <= interval.start:
                heapq.heappop(using_end_times)
            
            if len(using_end_times) == num_required_rooms:
                num_required_rooms += 1
            heapq.heappush(using_end_times, interval.end)
        return num_required_rooms

```

## step3

この形で練習しました。

```python

import heapq


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        num_required_rooms = 0
        using_end_times = []
        for interval in sorted(intervals, key=lambda x: x.start):
            while using_end_times and using_end_times[0] <= interval.start:
                heapq.heappop(using_end_times)
            
            if len(using_end_times) == num_required_rooms:
                num_required_rooms += 1
            heapq.heappush(using_end_times, interval.end)
        return num_required_rooms


```