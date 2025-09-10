# 各要素の数を数えるときの書き方の比較

- コードを読むときに驚かないように、複数の書き方で書いてみたものを残しています。

## if 文を使った書き方

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1
        
        top_k_frequent = sorted(num_to_count.items(), key=lambda item: item[1], reverse=True)[:k]
        return [num for num, _ in top_k_frequent]

```

## defaultdict を使った書き方

- https://docs.python.org/3/library/collections.html#collections.defaultdict

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = defaultdict(int)
        for num in nums:
            num_to_count[num] += 1
        
        top_k_frequent = sorted(num_to_count.items(), key=lambda item: item[1], reverse=True)[:k]
        return [num for num, _ in top_k_frequent]

```

## setdefault を使った書き方

- https://docs.python.org/3/library/stdtypes.html#dict.setdefault

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            num_to_count.setdefault(num, 0)
            num_to_count[num] += 1
        
        top_k_frequent = sorted(num_to_count.items(), key=lambda item: item[1], reverse=True)[:k]
        return [num for num, _ in top_k_frequent]

```

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            num_to_count[num] = num_to_count.setdefault(num, 0) + 1
        
        top_k_frequent = sorted(num_to_count.items(), key=lambda item: item[1], reverse=True)[:k]
        return [num for num, _ in top_k_frequent]

```

- set ですが、値が返ってくることを忘れないように

## get を使った書き方

- https://docs.python.org/3/library/stdtypes.html#dict.get

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            num_to_count[num] = num_to_count.get(num, 0) + 1
        
        top_k_frequent = sorted(num_to_count.items(), key=lambda item: item[1], reverse=True)[:k]
        return [num for num, _ in top_k_frequent]

```

## counter を使った書き方

- https://docs.python.org/3/library/collections.html#collections.Counter

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = Counter(nums)
        top_k_frequent = num_to_count.most_common(k)
        return [num for num, _ in top_k_frequent]

```

## 感想

- 今のところは if 文を使って書くのが自分にあっているかなと思います。