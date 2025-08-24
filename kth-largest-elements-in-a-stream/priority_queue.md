
## 最初に書いたもの

- 記録用に残しています。min-heap を意識しています。まずは、要素の追加と最小要素の取り出し操作を実装することを考えました。push は、木の最後に追加した要素を、ヒープ条件を満たすまで上に押し上げていくようにしました。pop は、木の最後の要素を根に移動させ、ヒープ条件を満たすまで下に下げていきます。

```python

class PriorityQueue:
    def __init__(self):
        self.a = []
        self.size = 0

    def push(self, val):
        self.a.append(val)
        self.size += 1
        index = len(self.a) - 1    
        while index >= 0:
            parent_index = (index - 1) // 2
            if parent_index < 0 or self.a[parent_index] < self.a[index]:
                break
            self.a[index], self.a[parent_index] = self.a[parent_index], self.a[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def pop(self):
        min_val = self.a[0]
        self.a[0] = self.a[self.size - 1]
        self.a.pop()
        self.size -= 1
        index = 0
        while True:
            smallest_index = index
            left_child_index = index * 2 + 1
            if left_child_index < self.size and self.a[left_child_index] < self.a[smallest_index]:
                smallest_index = left_child_index
            right_child_index = index * 2 + 2
            if right_child_index < self.size and self.a[right_child_index] < self.a[smallest_index]:
                smallest_index = right_child_index
            if index == smallest_index:
                break
            self.a[index], self.a[smallest_index] = self.a[smallest_index], self.a[index]
            index = smallest_index
        return min_val

```

## 整理したもの1

- 記録用に残しています。変数名を整理しました。

```python

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        index_to_fix = len(self.a) - 1
        while index_to_fix > 0:
            parent_index = (index_to_fix - 1) // 2
            if self.heap[parent_index] < self.heap[index_to_fix]:
                break
            self.heap[index_to_fix], self.heap[parent_index] = self.heap[parent_index], self.heap[index_to_fix]
            index_to_fix = parent_index

    def pop(self):
        min_value = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        index_to_fix = 0
        while True:
            smallest_index = index_to_fix
            left_child_index = index_to_fix * 2 + 1
            if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest_index]:
                smallest_index = left_child_index
            right_child_index = index * 2 + 2
            if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest_index]:
                smallest_index = right_child_index
            if index_to_fix == smallest_index:
                break
            self.heap[index_to_fix], self.heap[smallest_index] = self.heap[smallest_index], self.heap[index_to_fix]
            index_to_fix = smallest_index
        return min_value

```

## 整理したもの2

### 参考にしたもの
- https://en.wikipedia.org/wiki/Priority_queue
- https://github.com/python/cpython/blob/3.13/Lib/heapq.py
    - heapq のライブラリ
- https://discord.com/channels/1084280443945353267/1192736784354918470/1194613857046503444
- https://github.com/cheeseNA/leetcode/pull/12/files#diff-c6777a9fa2a76ba32d4ae096defc242cccf5837a82b89498073634d9402e49a9
    - pop 関数の while 文の終了条件を「左の子が存在しない場合」にするのもいいなと思いましたが、「子が存在しない場合」の方が少し自分の中で自然だと感じました。また、pop 関数内で最小の要素を見つける処理において、右の子と左の子のうちの小さい方を見つけた後、修正対象の要素と比較した方が見通しが良くなっているなと思いました。
- 命名規則について
    - https://peps.python.org/pep-0008/#descriptive-naming-styles
        > weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    - https://docs.python.org/3/tutorial/classes.html#private-variables
        > a name prefixed with an underscore (e.g. _spam) should be treated as a non-public part of the API (whether it is a function, a method or a data member)

```python

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def _has_left_child(self, position):
        return position * 2 + 1 < len(self.heap)

    def _has_right_child(self, position):
        return position * 2 + 2 < len(self.heap)

    def _has_child(self, position):
        return self._has_left_child(position)

    def _get_left_child_position(self, index):
        return index * 2 + 1

    def _get_right_child_position(self, index):
        return index * 2 + 2

    def _get_parent_position(self, index):
        return (index - 1) // 2

    def _get_smaller_child_position(self, position):
        smaller_child_position = self._get_left_child_position(position)
        if (
            self._has_right_child(position)
            and self.heap[self._get_right_child_position(position)]
            < self.heap[smaller_child_position]
        ):
            smaller_child_position = self._get_right_child_position(position)
        return smaller_child_position

    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def top(self):
        return self.heap[0]

    def size(self):
        return len(self.heap)

    def push(self, val):
        position_to_fix = len(self.heap)
        self.heap.append(val)
        position_to_fix = len(self.heap) - 1
        while position_to_fix > 0:
            parent_position = self._get_parent_position(position_to_fix)
            if self.heap[parent_position] < self.heap[position_to_fix]:
                break
            self._swap(position_to_fix, parent_position)
            position_to_fix = parent_position

    def extract_min(self):
        smallest = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        position_to_fix = 0
        while self._has_child(position_to_fix):
            smaller_child_position = self._get_smaller_child_position(position_to_fix)
            if self.heap[position_to_fix] < self.heap[smaller_child_position]:
                break
            self._swap(position_to_fix, smaller_child_position)
            position_to_fix = smaller_child_position
        return smallest


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.top_k_size = k
        self.top_k_scores = PriorityQueue()
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        self.top_k_scores.push(val)
        if self.top_k_scores.size() > self.top_k_size:
            self.top_k_scores.extract_min()
        return self.top_k_scores.top()

```

## 感想

- priority queue の実装だけを考えているときは、size と top 関数は必要ないかなと考えてしまいましたが、実際に使ってみるとやっぱりほしいなと思いました。作るだけじゃなくて、それを実際に使ってみるところまでやってみてよかったと思いました。
- 変数名と関数名が少し長くなってしまったなと感じており、どうにかできないかもう少し考えてみようと思います。