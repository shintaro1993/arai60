# 347. Top K Frequent Elements

## Step1

- 考えたこと
    - 各要素の個数を数えて、それを個数の多い順に並べて、上から k 個を選択する

### ソートを使った方法

- 見積り
    - 時間計算量：O(nlogn)
    - 空間計算量：O(n)

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

### heap を使った方法

- heapq は min-heap なのでどうしようか考えましたが、nlargest を使うのが自然かと思いました。

- 見積り：
    - 時間計算量：O(nlogk)
    - 空間計算量：O(n)

- nlargest の計算量の理解があいまいだと感じたので source code を調べて見ました。heap に保存する要素の数は k 個のみであると書かれていることを確認しました。
    - https://github.com/python/cpython/blob/39b2f82717a69dde7212bc39b673b0f55c99e6a3/Lib/heapq.py#L395

- nlargest を使うときに指定した n が iterable のサイズより大きい場合sorted[:n]を使って結果を返却している。確かに、すべての要素を大きい順に並べて返す、のであればヒープを使わずにソートするのが自然だなと思った。
    - https://github.com/python/cpython/blob/e140e6ef789b1d8de1afd715503740e96e5ae925/Lib/heapq.py#L542-L543

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1

        top_k_frequent = heapq.nlargest(k, num_to_count.items(), key=lambda item: item[1])
        return [num for num, _ in top_k_frequent]

```

- heap に追加するタプルの count の符号を反転させる方法も考えましたが、少しその場しのぎのような感じがしました。

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1

        heap = []
        for num, count in num_to_count.items():
            heapq.heappush(heap, (-count, num))
            
        top_k_frequent = []
        for _ in range(k):
            _, num = heapq.heappop(heap)
            top_k_frequent.append(num)
        
        return top_k_frequent
            
```

- 問題文に、返却するリストは「in any order」でよいと書かれていて、これを見逃していました。

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1

        top_k_frequent = []
        for num, count in num_to_count.items():
            heapq.heappush(top_k_frequent, (count, num))
            if len(top_k_frequent) > k:
                heapq.heappop(top_k_frequent)
        
        return [num for _, num in top_k_frequent]

```

- defaultdict を使う場合を考えたとき、setdefault との使い分けが気になり調べてみました。結果として、辞書に追加する処理が終わった後、ある key が存在しているか確認したいときに、defaultdict ではなく、setdefault の方が使いやすそうという認識を持ちました。
    - [Use cases for the 'setdefault' dict method](https://stackoverflow.com/questions/3483520/use-cases-for-the-setdefault-dict-method)

- 他の書き方で書かれたコードを読むときの助けになるように、dict の get, setdefault や defaultdict, counter を使った書き方を、practice.md に残しました。

## Step2

### 調べたこと

- https://discord.com/channels/1084280443945353267/1183683738635346001/1185972070165782688
    - quick select の話題がありましたが、自分の中でまだ整理できていないので、復習をするときに quick sort と合わせて整理しようと思います。
- https://discord.com/channels/1084280443945353267/1227073733844406343/1231286694758846464
    - 平衡木も普通のデータ構造とのことなので、こちらも復習のときに整理しようと思います。
- https://github.com/katataku/leetcode/pull/9#discussion_r1860305454
    - `sorted(count_frequency, key=count_frequency.get, reverse=True)[:k]` を見たときに、ソート結果の値がタプルから辞書のキーに置き換えられたのかと驚いたが、`count_frequency.items()`と見間違えていました。sorted に辞書をそのまま渡すと、キー同士が比較され、それらが結果として帰ってくるという動作を知りました。
    - これは、sorted 関数は iterable を引数にとり、そして、辞書に iter() next() を使うと、key が返ってくるので、sorted はこの操作で返ってくるものをソートの対象としているのかなと思いました。
        - https://docs.python.org/3/library/functions.html#sorted
- https://github.com/Fuminiton/LeetCode/pull/9/files
    - 自分は気づかなかったが、sorted の引数の指定が長くなったときに複数行に分けているのがいいなと思いました。
- https://github.com/TORUS0818/leetcode/pull/11/files
    - コードの見た目ですが、defaultdict を使うのも、すっきりしていいなと思いました。結果を返すときに、一度変数に置くかどうか悩ましいなと思いました。

- heapq モジュールを使うのであれば、nlargest を使いたくない理由が自分の中で見つからなかったので、こちらの方がシンプルにかけてよいと思いました。状況に応じて、ソートと使い分けれるようになればと思います。コードが複雑になったりしたら、デバッグするときのことを考えて return する前に変数に置くことも考えようかなと思います。

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1

        return heapq.nlargest(k, num_to_count, key=num_to_count.get)

```

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = {}
        for num in nums:
            if num not in num_to_count:
                num_to_count[num] = 1
                continue
            num_to_count[num] += 1
        
        return sorted(num_to_count, key=num_to_count.get, reverse=True)[:k]

```

## Step3

- 書いているうちに、defaultdict を使ってもいいかなという気持ちになり、こちらに変更しました。

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        num_to_count = defaultdict(int)
        for num in nums:
            num_to_count[num] += 1

        return heapq.nlargest(k, num_to_count, key=num_to_count.get)

```

## 感想

- これまでの練習では、選択肢を広げることを意識して取り組んできて、それは意識として少しずつ育ってきているかなと思い始めてきましたが、step3 でもう少し自信をもって自分の考えを提案できるようにしたいと思いました。なので、今後は、何をもって他の人たちがよしあしの判断をしているのかというところに注目して練習していこうと思いました。