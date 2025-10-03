# 153. Find Minimum in Rotated Sorted Array

## step1

とりあえず、一回も回転していない場合は除いて、リストの中に nums[0] 以上の要素が並んだ領域（ソート済み）と、nums[0] 未満の要素が並んだ領域（ソート済み）があると考える。そうすると、最小値は、nums[0] 未満の要素が並んだ領域の左端の要素になるので、これを見つけたい。nums[:index] のすべての要素が nums[0] 以上であり、nums[index:] のすべての要素が nums[0] 未満である条件を満たす index を探すとよさそう。

これまでに見つけた nums[0] 以上の要素が left より左に来ることを、これまでに見つけた nums[0] 未満の要素が right を含む右側に来ることを保証するようにする。left を0で、right を len(nums) で初期化し、まだ何も見つかっていない状態を表現したい。探索空間は [left, right) で考える。各ループの中で調べる場所を middle = (left + right) // 2 で計算して求める。left <= middle < right なので、各ループの中で探索空間の中から調べる要素を見つけられる。

nums[middle] が nums[0] 以上の場合、それがソート済みの nums[0] 以上の要素が並んだ領域に存在することが分かり、[left, middle] の領域のすべての要素が nums[0] 以上のため left を middle + 1 で更新する。nums[middle] が nums[0] 未満の場合、それがソート済みの nums[0] 未満の要素が並んだ領域に存在することが分かり、[middle, right) の領域のすべての要素が nums[0] 未満のため right を middle で更新する。left = middle + 1, right = middle で更新しているので作業の終わりで探索空間が1以上減少する。while で left < right を指定することで探索空間の中のすべての要素を見つけるとループが終了する。このとき、left == right になる。
ループが終わったとき、リスト内の nums[0] 以上であるすべての要素が nums[:left] にあり、nums[0] 未満のすべての要素が nums[left:] に存在している、つまり left - 1 の場所に最大値が、left の場所に最小値があるので最後に left の場所にある要素を返す。

nums が空の場合は別途処理を考えるとよさそう。

```python

class Solution:
    def findMin(self, nums: List[int]) -> int:
        if nums[0] <= nums[-1]:
            return nums[0]
        
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] >= nums[0]:
                left = middle + 1
            else:
                right = middle
        return nums[left]

```

一回も回転していない場合といいつつ、入力のリストの要素が1つの場合ものぞいていたことに後で気づいた。自分が何をやっているかは把握するようにしよう。

この方法だと、一回も回転していない場合、nums[:left] の領域にすべての要素がある left を見つけることになりうまくいかない。一回も回転していない場合に、すべての要素が nums[left:] にあるような left を見つけられるとよさそう。nums[-1] 以下とより大きいで分類して、nums[:left] に nums[-1] より大きなすべての要素が、nums[left:] に nums[-1] 以下のすべての要素があるような left を見つける方針に変える。

```python

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[-1] < nums[middle]:
                left = middle + 1
            else:
                right = middle
        return nums[left]

```

step1 の `if nums[middle] >= nums[0]` は `if nums[0] <= nums[middle]` の方が読みやすい気がしてきたけどどうだろう。
https://github.com/python/cpython/blob/3.13/Lib/bisect.py
    - bisect_left や bisect_right の hi について、hi は探索空間を含んでいないのかと思ったけど、insertion point は hi の場所を取りうるので、hi = len(a) と書いて閉区間を表現しているのかもしれないということが気になった。

## step2

## 調べたこと

- https://discord.com/channels/1084280443945353267/1230079550923341835/1233805817073897533
    > この問題、隣り合う a, b で、nums[a] > nums[b] となるものを探せ、ということだと思うと、閉区間でとるほうが自然かしら。
    - 考え方は複数あるということですね。

- https://discord.com/channels/1084280443945353267/1230079550923341835/1233971372946882600
    > nums[0] <= nums[i] な領域と nums[0] > nums[i] な領域の境界を探せ
    > nums[-1] < nums[i]  な領域と nums[-1] >= nums[i] な領域の境界を探せ
    - 前者の場合、回転していない場合を特別扱いせずにできるのかわからない

- https://discord.com/channels/1084280443945353267/1230079550923341835/1235694567085576275
- https://discord.com/channels/1084280443945353267/1192736784354918470/1235596462084067369
    - bisect_right を使う場合について、nums が回転していない場合は lo が len(nums) で初期化した hi のところまで動くので - len(nums) をすることで先頭を返せる。回転している場合は、- len(nums) をすると、後ろから数えたことになって元の場所まで戻ってくるので問題ない、という理解。そうすると、step1 のはじめで書いたコードも同じように修正できそうな気がする。
        - https://github.com/python/cpython/blob/a461f25ce66209b010f74e97890c051170142e4b/Lib/bisect.py#L21

- https://discord.com/channels/1084280443945353267/1322513618217996338/1349688711759003650
    > 「左側、つまり、条件を満たさないことが判明している左側の最大の場所」か
    > 「左側、つまり、条件を満たさないことが判明していない左側の最小の場所」
    - 自分はどちらかというと後者の考えかもしれない。

- https://github.com/ryosuketc/leetcode_arai60/pull/31/files#r2165564827
    > > left は、それより左は条件を満たさないことが保証されているんですよね。ということは最後まで探索が終わったとき left より左側はすべて条件を満たさない = すべて F、でleft の位置は最初の T を指しているはずだ、という理解をしました。
    - この説明しっくり来た。
    - right を len(nums) - 1 で初期化して、while の条件を left < right にしていると、探索空間に未発見の要素が一つ残っている状態でループが終了している気がするので自分はそうしないと思うけど、もう少し他の人が何をしようとして何を選択したのかを気にしながらコードを読んでいくと考えは変わるのかな。

- https://discord.com/channels/1084280443945353267/1245404801177616394/1308622011601518623
    > 「2で割る処理がありますがこれは切り捨てでも切り上げでも構わないのでしょうか。」
    > 「nums[middle] <= nums[right] とありますが、これは < でもいいですか。」
    > 「nums[right] は、nums[nums.length - 1] でもいいですか。」
    > 「right の初期値は nums.length でもいいですか。」
    - 質問を自分用に読み替えよう。
        - 切り上げると middle が right を指すときに探索空間の外に出るので困る。
        - そもそも nums[right] にすると配列外を参照してしまう。< でもいい場合がある。
        - 次の質問とも被るが、right を len(nums) - 1 で初期化すると、nums[right] でも大丈夫な場合がある。

- https://github.com/seal-azarashi/leetcode/pull/39#discussion_r1846593786
    > 1. 入力はこういう制約のものである
    > 2. そこに、left, right という変数を置く、これはこういう不変条件を満たす変数である
    > 3. ループを回すときに、middle という位置について計算をする、それは left, right との大小関係等こういう性質を持っている
    > 4. middle での値によって、left, right をこのように更新すると、不変条件を満たしたままにできる
    > 5. 更新をしていくと while をこういう条件で抜ける、この際にある式で表される値は left, right の不変条件から求めるものになっている
    > 6. これが必ず停止することは、ある値が狭義単調減少であることから言える
    - 6の「ある値」は探索空間のことであってるかな。

調べるとたくさん出てくるので、徐々に整理していくことにしよう。

以下，条件を満たす領域の左端を見つけると考えると、その条件を明示して先に持ってくる方が自然な気がしてきたので修正。

```python

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] <= nums[-1]:
                right = middle
            else:
                left = middle + 1
        return nums[left]

```

bisect_right を使って書かれたコードを参考にすることで step1 のコードを修正できたけど、nums[0] ではなく nums[-1] に注目する方が自然かな。

```python

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] >= nums[0]:
                left = middle + 1
            else:
                right = middle
        return nums[left - len(nums)]

```

## step3

この形で練習しました。

```python

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] <= nums[-1]:
                right = middle
            else:
                left = middle + 1
        return nums[left]

```

区間に境界が含まれるという話がどういうことなのかイメージできていない気がするので後で調べよう。そもそも境界という言葉とその表現のしかたを理解できていない気がする。
https://github.com/yamashita-ki/codingTest/pull/13#discussion_r2396353508