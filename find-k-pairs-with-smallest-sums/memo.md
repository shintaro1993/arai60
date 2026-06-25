# 373. Find K Pairs with Smallest Sums

## Step1

- 2つの配列において作れるすべての組み合わせのペアの中から、各ペアの和が小さい方から k 個選んで、それら k 個のペアを返す。

- まずは単純にすべてのペアを作ってみようと思います。

- 見積り：
    - n: len(nums1)
    - m: len(nums2)
    - 時間計算量：O(n*m)
    - 空間計算量：O(n*m)

```python

# 以下の２つのコードは LeetCode 上で 「Memory Limit Exceeded」になります。

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = []
        for num1 in nums1:
            for num2 in nums2:
                pairs.append([num1, num2])
        return sorted(pairs, key=sum)[:k]

```

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        pairs = []
        for num1 in nums1:
            for num2 in nums2:
                pairs.append([num1, num2])
        return heapq.nsmallest(k, pairs, key=sum)

```

- 直積を求める書き方が複数あると思ったので、その書き方の練習を practice.md に残しています。

- 今回は、それぞれの配列のサイズを最大10の5乗まで想定することになっていて、ペアを作る段階でメモリエラーになりそうなのでそこをまず改善しようと思います。

- nums1 のすべての要素が、まず最初にペアを組みたい相手は nums2[0] 。nums2[1] とペアを組むのは、nums2[0] とのペアが、返却用のリストに追加された後でいいです。
- nums1 のすべての要素と nums2[0] の要素でペアを作り、初期値としてヒープに入れておく。ヒープから和の最小値のペアが取り出されるごとに、取り出したペアの nums1 の要素はそのままで、nums2 の要素は次のものにしたペアをヒープに追加する。ヒープには初期値として nums1 と nums2 のリストのサイズが小さいほうで初期化し、ヒープから一つ取り出すごとに一つ追加していくので、この処理の最中に使うメモリは初期化したサイズで考えてよさそうだと思います。全体としては、返却用のリストを作っているので空間計算量は O(k) になるでしょうか。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        candidates = []
        for i in range(len(nums1)):
            heapq.heappush(candidates, (nums1[i] + nums2[0], i, 0))

        result = []
        while len(result) < k:
            _, i, j = heapq.heappop(candidates)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(candidates, (nums1[i] + nums2[j+1], i, j + 1))

        return result

```

- 次に制約では入力のリストのサイズは１以上であることが保証されていますが、空のリストが与えられた場合の動作について考えます。
- 試しに nsmallest のコードの確認と実験をしてみたら、空のリストが与えられたときは空のリストが返ってきていました。私も今回は k が0の場合も含めて空のリストを返すということでいいかなと思います。
    - https://github.com/python/cpython/blob/b220c1c0a479fdb362d97735034f7ce2edf1e3db/Lib/heapq.py#L491-L492
- 返却するリストのサイズが k より少ない場合は、できてるものだけでも返した方が使いやすいと思いました。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2 or k == 0:
            return []

        candidates = []
        for i in range((len(nums1))):
            heapq.heappush(candidates, (nums1[i] + nums2[0], i, 0))

        result = []
        while candidates and len(result) < k:
            _, i, j = heapq.heappop(candidates)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(candidates, (nums1[i] + nums2[j+1], i, j + 1))

        return result

```

- nums2 が空の場合だけチェックすれば動きますが、nums1 と k についてもここに書いておいた方が、読んでいる人に意図が伝わりやすいかと思いました。
- リストの参照に使う i と j については他にも良い名前がありそうですが、そちらは調べてみようと思います。

## Step2

### 発想関連について調べたこと

- https://discord.com/channels/1084280443945353267/1196472827457589338/1196541234169266387
    - heap の初期値を (nums1[0] + nums2[0], 0, 0) だけにする方法もあるそうなので、考えてみます。
- https://discord.com/channels/1084280443945353267/1201211204547383386/1206515949579145216
    > index1 >= len(nums1) としたら、index1 が nums1 の上を走る変数であることが明確です。
    - 私も、意図と操作のつながりをもっと意識しようと思いました。

- https://discord.com/channels/1084280443945353267/1251052599294296114/1253232809062170675
- https://discord.com/channels/1084280443945353267/1231966485610758196/1268091954537959437
    - 自然言語での説明方法や発想について整理できていない部分を整理する

- `heap の初期値を (nums1[0] + nums2[0], 0, 0) だけにする方法` について考えます。これは異なる発想の話かと思いましたが、自分の中では各 i について、(nums1[i] + nums2[0], i, 0) をどのタイミングでヒープに追加するか考える問題としてとらえました。追加するタイミングは、(nums1[i-1] + nums2[0], i-1, 0) がヒープからポップされたタイミングで大丈夫だと思い、以下のようなコードに修正しました。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        result = []
        candidates = [[nums1[0] + nums2[0], 0, 0]]
        while candidates and len(result) < k:
            _, i, j = heapq.heappop(candidates)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(candidates, (nums1[i] + nums2[j+1], i, j + 1))
            if j == 0 and i + 1 < len(nums1):
                heapq.heappush(candidates, (nums1[i+1] + nums2[0], i + 1, 0))
        return result

```

- ヒープに追加する処理は関数にした方が読みやすいかなと思いました。二つ目の if 文の条件の順番も入れ替えて一つ目とそろえた方が目にやさしく感じました。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        def push_to_candidates_if_needed(index1: int, index2: int) -> None:
            if index2 + 1 < len(nums2):
                heapq.heappush(
                    candidates, (nums1[index1] + nums2[index2 + 1], index1, index2 + 1)
                )
            if index1 + 1 < len(nums1) and index2 == 0:
                heapq.heappush(
                    candidates, (nums1[index1 + 1] + nums2[0], index1 + 1, 0)
                )

        result = []
        candidates = [[nums1[0] + nums2[0], 0, 0]]
        while candidates and len(result) < k:
            _, i, j = heapq.heappop(candidates)
            result.append([nums1[i], nums2[j]])
            push_to_candidates_if_needed(i, j)
        return result

```

### 他の方のコードを読む

- https://github.com/Mike0121/LeetCode/pull/20/files
    - DFS を連想することもできるのですね。いろいろと書き換えられており、選択が難しそうだなと思いました。
- https://github.com/fhiyo/leetcode/pull/13/files
    - 自分と似たような考え方でコードを書かれていると思ったが、while ではなく for 文を使うと全体の印象が少し違っている。自分が気になっていた heappush の引数の扱いについて、関数で処理をされていて自分も参考にしようと思った。関数名は好みで少し変えます。
- https://github.com/nittoco/leetcode/pull/33/files
    - 自分も new_index に置きたい気持ちはあるが難しいところ
- https://github.com/olsen-blue/Arai60/pull/10/files
    - なるほど、処理を関数に切り出したときに i, j で受け取ると、個人的に読みにくいかもしれない。
- https://github.com/quinn-sasha/leetcode/pull/10/files
    - 今は意図が分かった状態で読んでいるが、引数に + 1 したりするのは間違えそうだなと感じた。メインループで呼び出す関数を二つに分けてもいいかもしれないと感じた。


```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        def get_sum_and_indexes(index1: int, index2: int):
            return nums1[index1] + nums2[index2], index1, index2

        def push_to_candidates_if_needed(index1: int, index2: int) -> None:
            if index2 + 1 < len(nums2):
                heapq.heappush(candidates, get_sum_and_indexes(index1, index2 + 1))
            if index1 + 1 < len(nums1) and index2 == 0:
                heapq.heappush(candidates, get_sum_and_indexes(index1 + 1, index2))

        k_smallest_pairs = []
        candidates = [[nums1[0] + nums2[0], 0, 0]]
        while candidates and len(k_smallest_pairs) < k:
            _, i, j = heapq.heappop(candidates)
            k_smallest_pairs.append([nums1[i], nums2[j]])
            push_to_candidates_if_needed(i, j)
        return k_smallest_pairs

```

- 自分の中で `push_pair_of_nums1_and_next_nums2` 関数の処理は、ヒープから取り出したら基本的に行う作業なので if 文の中で行うことに違和感がありました。関数名との兼ね合いも難しく、時間をおいて見直した方がいいと思いました。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        def get_sum_and_indexes(index1: int, index2: int):
            return nums1[index1] + nums2[index2], index1, index2

        def push_pair_of_nums1_and_next_nums2(index1, index2):
            if index2 + 1 >= len(nums2):
                return
            heapq.heappush(candidates, get_sum_and_indexes(index1, index2 + 1))

        def push_pair_of_next_nums1_and_smallest_nums2(index1, index2):
            if index2 == 0 and index1 + 1 < len(nums1):
                heapq.heappush(candidates, get_sum_and_indexes(index1 + 1, index2))

        k_smallest_pairs = []
        candidates = [[nums1[0] + nums2[0], 0, 0]]
        while candidates and len(k_smallest_pairs) < k:
            _, i, j = heapq.heappop(candidates)
            k_smallest_pairs.append([nums1[i], nums2[j]])
            push_pair_of_nums1_and_next_nums2(i, j)
            push_pair_of_next_nums1_and_smallest_nums2(i, j)
        return k_smallest_pairs

```

## Step3

- コードを書きあげる練習をしているうちにこの形に落ち着きました。

```python

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        def get_sum_and_indexes(index1: int, index2: int) -> Tuple[int, int, int]:
            return nums1[index1] + nums2[index2], index1, index2

        def push_nums1_and_next_nums2(index1: int, index2: int) -> None:
            if index2 + 1 >= len(nums2):
                return
            heapq.heappush(candidates, get_sum_and_indexes(index1, index2 + 1))

        def push_next_nums1_and_smallest_nums2(index1: int, index2: int) -> None:
            if index2 == 0 and index1 + 1 < len(nums1):
                heapq.heappush(candidates, get_sum_and_indexes(index1 + 1, index2))

        k_smallest_pairs = []
        candidates = [[nums1[0] + nums2[0], 0, 0]]
        while candidates and len(k_smallest_pairs) < k:
            _, i, j = heapq.heappop(candidates)
            k_smallest_pairs.append([nums1[i], nums2[j]])
            push_nums1_and_next_nums2(i, j)
            push_next_nums1_and_smallest_nums2(i, j)
        return k_smallest_pairs

```

## 感想

- 不自然なのか不自然じゃないのかを言語化できずにモヤモヤする時間が気になったので、そういう時は Step3 に行く前に何も見ずにコードを書けるかどうか試してみて、その結果を判断の材料にしてみるとよさそうだと思ったので次回からそうしようと思う。