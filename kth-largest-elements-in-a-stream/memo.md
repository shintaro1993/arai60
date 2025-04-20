# 703. Kth Largest Element in a Stream

## Step1

- まずは動くコードを書いてみます。今までとやり方を変えて、動くコードを書いた後、discord 内を調べる前に気になるところをある程度整理しておこうと思います。

### 考えたこと

- ストリームすべてを降順のリストで管理します。add が呼ばれたときに、リストが降順である状態を保ったまま挿入を行います。

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums, reverse=True)

    def insert_val_still_descending_order(self, nums: List[int], val: int):
        for i in range(len(self.nums)):
            if val >= nums[i]:
                nums.insert(i, val)
                return
        nums.append(val)
        
    def add(self, val: int) -> int:
        self.insert_val_still_descending_order(self.nums, val)
        index = self.k - 1
        if len(self.nums) < self.k:
            index = -1
        return self.nums[index]

```

- 見積り
    - add が呼ばれた回数と初期化するときに与えられたリストのサイズの合計を n と考えます。
    - 時間計算量：O(n)
    - 空間計算量：O(n)

- add が呼び出されるたびにリストの要素が増えていることが気になりました。使っているといつかメモリエラーが起きそうだなと思ったので実際にリストのサイズはどのくらいまで大きくできるのか実験しようと思いました。ループの中でサイズが 10^6 のリストを作って、初期化しておいた空のリストに extend していく実験をしました。プロセスは kill されましたが Python の MemoryError で補足できなかったので調べてみたら Linux がプロセスを kill していたようでした。リストのサイズが 4GB くらいになったところで kill されていることがわかりました。
    - [Finding which process was killed by Linux OOM killer [closed]](https://stackoverflow.com/questions/624857/finding-which-process-was-killed-by-linux-oom-killer)
        - (a = a + b よりも a.extend(b) を使った方がはやかったので、また後でいろいろ実験してみよう) 

- 使うデータは上位 k 個の要素だけなので、それだけを管理していくようにしたいと思います。
- データ構造に 1) list を使う方法と、2) heap を使う方法を使う方法を考えました。

### list でデータを降順で保存する方法

- `sorted(nums, reverse=True)[:self.k]` の部分を `self.nums = heapq.nlargest(k, nums)` に変更することもできる。指定するサイズが大きい時は前者の方が efficient で、小さい時は後者が efficient と書かれている。
    - https://docs.python.org/3/library/heapq.html

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums, reverse=True)[:self.k]

    def insert_val_still_descending_order(self, nums, val):
        for i in range(len(nums)):
            if val >= nums[i]:
                nums.insert(i, val)
                return
        nums.append(val)
        
    def add(self, val: int) -> int:
        self.insert_val_still_descending_order(self.nums, val)
        if len(self.nums) > self.k:
            self.nums.pop()
        return self.nums[-1]

```

- この実装だと、nums の大きさが k よりも大きい場合、k よりも大きなコピーが作られる

### list でデータを昇順で保存する方法

- 昇順のリストでの挿入なので、二分探索を連想しました。insort は、挿入する場所を探すのに bisect_right() を使い、要素の挿入に insert() を使っているようです。
    - https://docs.python.org/3/library/bisect.html#bisect.insort_right

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums)[-self.k:]
        
    def add(self, val: int) -> int:
        bisect.insort(self.nums, val)
        if len(self.nums) > self.k:
            self.nums.pop(0)
        return self.nums[0]

```

### heap でデータを保存する方法

- インスタンスを初期化するときに渡されたリストのサイズを n と考えます。
- 見積り
    - 時間計算量：O(nlogk)
    - 空間計算量：O(n)

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = []
        for num in nums:
            heapq.heappush(self.nums, num)
        while len(self.nums) > self.k:
            heapq.heappop(self.nums)

    def add(self, val: int) -> int:
        heapq.heappush(self.nums, val)
        if len(self.nums) > self.k:
            heapq.heappop(self.nums)
        return self.nums[0]

```

- 初期化するときに入力の配列のサイズのコピーを作っているので、サイズを k に抑える書き方も試してみます。

- 見積り
    - 時間計算量：O(nlogk)
    - 空間計算量：O(k)

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        heapq.heappush(self.nums, val)
        if len(self.nums) > self.k:
            heapq.heappop(self.nums)
        return self.nums[0]

```

- heappush() の後に heappop() をする場合、heappushpop()に置き換えることでより効率的になるとドキュメントに書いてあったので、これを使った書き方も試してみる。 
    - https://docs.python.org/3/library/heapq.html#heapq.heappushpop

```python

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        if len(self.nums) >= self.k:
            heapq.heappushpop(self.nums, val)
        else:
            heapq.heappush(self.nums, val)
        return self.nums[0]

```

## Step2

### 調べたこと

- https://github.com/katataku/leetcode/pull/8
    - ある実装でスライスを使っていて、そこで初期化するときに渡される k が負の値のときに、どのような動作をしてほしいかというところまで考えられていなかった。まずは自分の想定の外側があることを意識して、そこにも興味を持つようにしよう。
- https://discord.com/channels/1084280443945353267/1200089668901937312/1203697318407315476
    - quickselect, counting sort で考えられた方もいるそうで、復習のときに改めて整理しようと思います。priority queueの実装も後でしようと思います。
- https://github.com/kazukiii/leetcode/pull/9/files#diff-a8f49f15620a56051718e3a0fd0046f718a21738a7b499e97d01f1f1cc3b0fb9
    - init で heap のサイズを k にするときに、for 文の中で heappush と heappop するかどうか判定しており、個人的には判定を for 文の外でした方が読みやすいかなと感じた。
- https://github.com/haniwachann/leetcode/pull/1/files
    - map を使って実装されている方もいる。
- https://github.com/tarinaihitori/leetcode/pull/8/files
    - heap を使った実装だと、だいたい同じようなコードに落ち着いている印象を持った。
- https://github.com/colorbox/leetcode/pull/23/files
    - 使う言語が変わると考えないといけないことも変わるのだなと感じた。

- priority_queue.md で、自分で作った priority queue でコードを書きました。

```python

- 見積り
    - 時間計算量：O(nlogk)
    - 空間計算量：O(k)

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.top_k_size = k
        self.top_k_scores = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        heapq.heappush(self.top_k_scores, val)
        if len(self.top_k_scores) > self.top_k_size:
            heapq.heappop(self.top_k_scores)
        return self.top_k_scores[0]

```

## Step3

- step2で書いたもので練習しました。
- ステップ3で0から書く練習をするとき、記憶力を使って書いている気がした。コードをよく見て、どのように自分の中にしまいたいか、取り出したいか考えた後に書く練習をした方がよさそう。コードを見るのはよくないことだと思わないようにしようと思います。