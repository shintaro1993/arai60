# 復習や宿題を整理する用です。

## 他の実装について

- https://discord.com/channels/1084280443945353267/1201211204547383386/1210788090973523968
    - ワンパスで解く方法。二回以上出てきたものは set で管理し、一回目だけのものを OrderDict で管理する

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        seen = set()
        unique_letter_to_index = {}
        for i, c in enumerate(s):
            if c in seen:
                if c in unique_letter_to_index:
                    del unique_letter_to_index[c]
                continue
            unique_letter_to_index[c] = i
            seen.add(c)

        if not unique_letter_to_index:
            return -1
        
        for letter, index in unique_letter_to_index.items():
            return index

```

- https://docs.python.org/3/library/stdtypes.html#dict.pop
    - 辞書の pop 関数。キーがない場合、初期値を渡すとそれを返してくれる。
- 返すときにループを使っているのを何とかしたい。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        seen = set()
        unique_letter_to_index = {}
        for i, c in enumerate(s):
            if c in seen:
                unique_letter_to_index.pop(c, None)
                continue
            unique_letter_to_index[c] = i
            seen.add(c)

        if not unique_letter_to_index:
            return -1

        it = iter(unique_letter_to_index)
        return unique_letter_to_index[next(it)]

```

- https://docs.python.org/3/library/collections.html#collections.OrderedDict
    - なるほどです。OrderedDict を使うと popitem で FIFI 順で取り出すようにすることもできるのですね。
- https://docs.python.org/3/library/stdtypes.html#dict.popitem
    - 辞書の popitem ではできない。

```python

class Solution:
    def firstUniqChar(self, s: str) -> str:
        seen = set()
        unique_letter_to_index = OrderedDict()
        for i, c in enumerate(s):
            if c in seen:
                unique_letter_to_index.pop(c, None)
                continue
            unique_letter_to_index[c] = i
            seen.add(c)
        if not unique_letter_to_index:
            return -1
        _, index = unique_letter_to_index.popitem(last=False)
        return index

```