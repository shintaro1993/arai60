# 514 · Paint Fence

n 個のポストを k 種類の色で塗る作業を考える。同じ色が隣に3個以上並んではいけないという条件を満たすすべての塗り方の数を求める。

https://www.lintcode.com/problem/514/discuss

## Step1

### approach a

まず、k^n 通りの塗り方をすべて作って、条件を満たしているものを数える方法を考えました。(./step1/approach_a.pyに作成済み)
すべての塗り方を樹形図のように書き出したものをイメージして、ルートから現在訪れているノードまでの塗り方をリストで管理しながら深さ優先探索をします。リストのサイズが n になったときに塗り方が条件を満たしているか調べます。(計算量は O(k^n*n) くらいで、実行時間は n=20 k=2 で 2秒くらいだった。)

ルートから現在訪れているノードまでの塗り方を変数 way で表現しましたが、実態は数値のリストで、変数名からはそれがリストであるということが分かりにくいかもしれません。意味としてはこの名前が分かりやすいと感じているので悩ましいと感じました。
リストのサイズが n になったときに条件を満たしているか調べるより、リストに追加するときに条件を満たさない場合をはじいていく方が自然かもしれない。

Python の関数で似たようなものを参考にできないかと思い、以下の関数を見つけました。どちらの関数も引数が integer かどうか調べていて、異なる場合は TypeError を投げています。また、どちらかの引数が負の値の場合 ValueError を投げていて、そのとき n と k のどちらが負の値なのか教えてくれて親切だと思いました。n が0のときは0が、k が0のときは1が返ってきます。エラーメッセージの書き方参考になりました。

- math.comb(n, k): https://docs.python.org/3/library/math.html#math.comb
- math.perm(n, k=None): https://docs.python.org/3/library/math.html#math.perm
> Raises TypeError if either of the arguments are not integers. Raises ValueError if either of the arguments are negative.

### approach b

ポストの塗り方について、直前で二つのポストが同じ色で塗られた場合の数と直前で二つのポストが異なる色で塗られた場合の数を更新していき、最後にそれらの和を返す、という方法を考えました。(./step1/approach_b.pyに作成済み)

ループ内の変数 new は、next と迷いましたが、更新した値であることを強調したかったので new にしました。

最初はループの中で以下のように書いていましたが、書き直した方が読みやすいと感じました。

```python

tmp = same_last_two
same_last_two = diff_last_two
diff_last_two = (tmp + diff_last_two) * (k - 1)

```

## Step2

### 調べたこと・読んだコード

- https://discord.com/channels/1084280443945353267/1200089668901937312/1205715212276342784
    - n=1やn=2の場合でもループに入っていて、自分ははやく return したいと感じた。
    - range で生成したインデックスを使ってい場合は、個人的には start と stop を調整して回すより start には何も指定しない方が好みだと思う。
    - 部分問題の解を使う方法もある。この考えがメモ化につながるのかな。
        - Dynamic programming: https://en.wikipedia.org/wiki/Dynamic_programming
    - TODO:
        - 「メモ化」について調べる
        - @cache を自作する: https://discord.com/channels/1084280443945353267/1200089668901937312/1206164658223058984
            - 内部で OrderDict が使われているそうなので、そちらも自作できれば

- https://discord.com/channels/1084280443945353267/1201211204547383386/1220427602356076665
    - 直前と同じ色を塗る場合と違う色を塗る場合で考えると動的計画法として考えやすくなったかもしれない。

- コメント集 - Python デコレータ: https://docs.g oogle.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.3ty938gr73xw

### approach c

部分問題を使って現在の問題を解決するという考えで書きました。(./step2/approach_c_1.pyに作成済み)
0-index と 1-index どちらでリストを使うか考えましたが、リストの初期化をサイズ n でした方が分かりやすく感じたので 0-index を採用しました。
memo という変数名は過去に計算したものを使いまわすという意図を込めて決めましたが、再帰をイメージする人がいるのかなと思い、変えるのも選択肢かなと思いました。

approach_c_1.py を再帰で書きなおし(./step2/approach_c_2.py)、それを functools の cache を使って書き替えました。(./step2/approach_c_3.py)
大まかなイメージができたので、以下で自作の cache を作ろうと思います。

cacheについて：
- @functools.cache(user_function): https://docs.python.org/3/library/functools.html#functools.cache
- @functools.lru_cache(user_function): https://docs.python.org/3/library/functools.html#functools.lru_cache
- lru_cache: https://github.com/python/cpython/blob/1a6e2138773b94fdae449b658a9983cd1fc0f08a/Lib/functools.py#L480

- https://github.com/fuga-98/arai60/pull/36#discussion_r2052146191
- https://github.com/shining-ai/leetcode/pull/40#discussion_r1550074736
- https://stackoverflow.com/questions/70836529/why-does-functools-cache-and-functools-lru-cache-not-working-for-inner-funct
    - クラスの inner 関数は、outer 関数の呼び出しごとに re-created される
- https://github.com/fuga-98/arai60/pull/35/files#r2044583200
    - クラスのメソッドの場合、同じインスタンスを再利用するとメモリ使用量が増えていく。異なるインスタンス間でも同じメソッドであればキャッシュは共有される認識だった。このあたりもう少し調べよう。

デコレータ:
- https://peps.python.org/pep-0318/
    - パラメータを指定する場合
    > The current syntax also allows decorator declarations to call a function that returns a decorator:
    > @decomaker(argA, argB, ...)
    > def func(arg1, arg2, ...):
    >     pass
    > This is equivalent to:
    > func = decomaker(argA, argB, ...)(func)
    - https://stackoverflow.com/questions/5929107/decorators-with-parameters?utm_source=chatgpt.com

- https://docs.python.org/3/glossary.html#term-decorator
    - クラスにもデコレータをつけれるらしい
    - https://docs.python.org/3/reference/compound_stmts.html#class-definitions

- callable: https://docs.python.org/3/library/functions.html#callable

調べものをした後 lru_cache を自作しました。(./step2/approach_c_4.py)
cpython では、リストでノードを表現していましたが、個人的に読みにくかったのでクラスを使いました。doubley linked list では node ではなく link という方が自然なのでしょうか。自分の書きやすさで、ダミーの head と tail と辞書を使って書きましたが、OrderdDict を参考にしてもよかったと思いましたので、復習しながらやってみます。(https://github.com/python/cpython/blob/23b7a95f41674fa949e1b415f82e4b8858db47ae/Lib/collections/__init__.py#L86)

※ lintcode 上では、submit 後 92% まで進んで止まってしまいます。n=1314520, k=1 のテストケースにおいて、自作のキャッシュと functools の lru_cache, cache のそれぞれのエラーメッセージに差異があるので改めて調べたい。

## Step3

(./step3/approach_b_2.py) で練習しました。
a * (k - 1) + b * (k - 1) よりは、(a + b) * (k - 1) の方が少し読みやすいかと感じました。

よくわかっていないことがそれなりにあるということが分かったことが収穫だったかもしれない。少し混乱している気がするので、時間をおいて他の人の PR をもっと読んでいく。
