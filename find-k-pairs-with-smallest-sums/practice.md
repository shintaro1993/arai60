# 練習

- 直積を求める書き方が複数あると思ったので、その書き方の練習を残しています。

## 内法表記を使う方法 

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = [[num1, num2] for num1 in nums1 for num2 in nums2]
        return sorted(pairs, key=sum)[:k]

```

- 慣れのせいかもしれませんが、読みやすさを感じていません。

## product を使う方法

- Cartesian product を作るのには product も使える。返ってくるのはジェネレータ式。
    - https://docs.python.org/3/library/itertools.html#itertools.product

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = [list(item) for item in product(nums1, nums2)]
        return sorted(pairs, key=sum)[:k]

```

- ということは、このようにするとペアの計算をするときに使うメモリを k にできるのでしょうか。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        return heapq.nsmallest(k, product(nums1, nums2), key=sum)

```

- LeetCode 上でのエラーが 「Time Limit Exceeded」に変わりました。
- ジェネレータ式の動作は復習するときに他にも実験をしてみます。

## 追記

- https://discord.com/channels/1084280443945353267/1235829049511903273/1246118347863621652
- https://discord.com/channels/1084280443945353267/1235829049511903273/1246303084435607682
- https://discord.com/channels/1084280443945353267/1226508154833993788/1270734186713710614
- https://github.com/nittoco/leetcode/pull/33#discussion_r1705967880
    - yield を使った実装実装もできるとのこと。自分もここまでつなげたかった。こちらも復習しながら動作確認します。
