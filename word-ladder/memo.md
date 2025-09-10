# 127. Word Ladder

## Step1

### 考えたこと

- 結果として返すための変数として result を用意して、1 で初期化する。(shortest transformation sequence)
- まず、startword と1文字だけ異なる文字列を wordlist からすべて取り出す。result をインクリメントする。
- 次に、取り出した単語すべてに対して、先ほどと同じように1文字だけ異なる単語をすべて wordlist から取り出す。result をインクリメントする。
- この作業を endword を取り出すまで続け、最後に、result を返す。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def can_transform(word1, word2):
            if len(word1) != len(word2):
                return False
            count = 0
            for i in range(len(word1)):
                if word1[i] != word2[i]:
                    count += 1
                    if count > 1:
                    return False
            return True

        result = 1
        words_before_transform = [beginWord]
        seen = set()
        seen.add(beginWord)

        while words_before_transform:
            n = len(words_before_transform)
            transformed_words = []
            for i in range(n):
                original_word = words_before_transform.pop()
                for word in wordList:
                    if word in seen:
                        continue
                    if can_transform(original_word, word):
                        transformed_words.append(word)
                        seen.add(word)        
                        if word == endWord:
                            return result + 1
            words_before_transform = transformed_words
            result += 1

        return 0

```

- 少し整えたもの
- zip 関数を使うと読みやすくなりそう
    - https://docs.python.org/3/library/functions.html#zip

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def can_transform(word1, word2):
            if len(word1) != len(word2):
                return False
            difference_count = 0
            for c1, c2 in zip(word1, word2):
                if c1 == c2:
                    continue
                difference_count += 1
                if difference_count > 1:
                   return False
            return True

        result = 1
        words_before_transform = [beginWord]
        seen = {beginWord}

        while words_before_transform:
            transformed_words = []
            for _ in range(len(words_before_transform)):
                original_word = words_before_transform.pop()
                for word in wordList:
                    if word in seen:
                        continue
                    if not can_transform(original_word, word):
                        continue
                    if word == endWord:
                        return result + 1
                    transformed_words.append(word)
                    seen.add(word)        

            words_before_transform = transformed_words
            result += 1

        return 0

```

- 見積り
    - n: len(startWord)
    - m: len(wordList)
    - 時間計算量: O(n*m^2)
    - 空間計算量: O(n*m)

- 見つけた単語は wordList から削除したかったが、以下のように書くと想定しない動作になるので、他の方法を考えたい。
- 入力の wordList 自体は壊さない方がよさそう。

```python

for word in wordList:
    # 省略
    transformed_words.append(word)
    seen.add(word)
    wordList.remove(word)

```

- https://docs.python.org/3/tutorial/controlflow.html#for-statements
    > Code that modifies a collection while iterating over that same collection can be tricky to get right. Instead, it is usually more straight-forward to loop over a copy of the collection or to create a new collection:
- strategy として、コピーを作る方法があるらしい。
- wordList を集合に変換して削除をしても `RuntimeError: Set changed size during iteration` というエラーが出る。

- 入力に英小文字以外が与えられた場合について考えると、beginWord と endWord に英小文字以外が含まれていると ValueError を投げて、wordList の中に英小文字以外が含まれている単語を見つけたときは、その単語を飛ばす、のが使いやすいだろうか。

- 少し変えたもの

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def can_transform(word1, word2):
            if len(word1) != len(word2):
                return False
            difference_count = 0
            for c1, c2 in zip(word1, word2):
                if c1 == c2:
                    continue
                difference_count += 1
                if difference_count > 1:
                   return False
            return True

        result = 1
        words_before_transform = [beginWord]
        seen = {beginWord}
        while words_before_transform:
            transformed_words = []
            for word in words_before_transform:
                if word == endWord:
                    return result
                for candidate in wordList:
                    if candidate in seen:
                        continue
                    if not can_transform(word, candidate):
                        continue
                    transformed_words.append(candidate)
                    seen.add(candidate)
            words_before_transform = transformed_words
            result += 1
        return 0

```

## Step2

### 調べたこと・読んだコード

- https://discord.com/channels/1084280443945353267/1200089668901937312/1216123084889788486
- https://github.com/hayashi-ay/leetcode/pull/42
    - 編集距離という用語や、「どれくらい時間がかかるか」見積もる方法を整理しておく
    - 書かれていたコードは LeetCode 上では Time Limit Exceeded になった。やっていること自体は自分と似ているコードだと思ったが、何が違うのだろうか。
        - このコードでは、編集距離が1の単語のリストを求めるとき、adj 関数内で wordList のループを回しているが、そこで seen を使っていなかった。そこに seen を持っていくと、とりあえず LeetCode 上でも動いた。ただ、どこでどれくらいの時間がかかっているかの理解が曖昧なので、少しずつ実行時間の見積もりの練習をしていこう。
    - hamming_distance という関数を用意して関数内では数だけ返して、呼び出し元でそれが1かどうか判定するというのがわかりやすいと感じた。
    - lru_cache を確認する
        - https://docs.python.org/3/library/functools.html#functools.lru_cache
- https://github.com/shining-ai/leetcode/pull/20/files
    - step1 のキューを使った実装について、キューに単語と距離をセットで保存すると、それらの対応関係が明確になり読みやすく感じた。自分のように return するときに + 1 するよりも読みやすい。
    - 辞書を使って高速化する方は、ワイルドカード表現をキーにして一文字違いの単語をリストに保存していく処理を事前に行い、幅優先探索中に次の移動先を見つける処理を高速にしているということかな。
    - step2 の隣接リストを使ったコードについて、返却用の変数を1で初期化して while ループのはじめのところでインクリメントするのは少し違和感があった。step3 ではこのタイミングを変更されていたので、同じ違和感を感じたのでしょうか。
    - 隣接リストを作るときに、入力で受け取った wordList に beginWord を追加しているのは少し違和感があるかも。
- https://discord.com/channels/1084280443945353267/1303605021597761649/1306631474065309728
    - yield を使った書き方はまた後で見返そう。変数の使い方などシンプルでいいなと思った。
- https://github.com/t0hsumi/leetcode/pull/20#discussion_r1938166243
    - path を管理していくという発想は思いつかなかった。
- https://github.com/olsen-blue/Arai60/pull/20/files
    - ワイルドカード表現の書き方がまだ整理できないので、書くのは今度にしよう。
- https://github.com/fhiyo/leetcode/pull/22/files
    - generator を使うのも後で書いてみよう。

- 隣接リストを使った方法が自分の中で自然な書き方だと思ったので、これで書いてみる

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
            
        def is_adjacent(word1, word2):
            if len(word1) != len(word2):
                return False
            differences = 0
            for c1, c2 in zip(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                   return False
            return True
        
        def create_adjacency_list(wordList, beginWord):
            adjacency_list = defaultdict(list)
            for i in range(len(wordList)):
                for j in range(i + 1, len(wordList)):
                    w1 = wordList[i]
                    w2 = wordList[j]
                    if is_adjacent(w1, w2):
                        adjacency_list[w1].append(w2)
                        adjacency_list[w2].append(w1)

            if beginWord in wordList:
                return adjacency_list

            for word in wordList:
                if is_adjacent(beginWord, word):
                    adjacency_list[beginWord].append(word)
                    adjacency_list[word].append(beginWord)
            return adjacency_list

        result = 1
        adjacency_list = create_adjacency_list(wordList, beginWord)
        words = [beginWord]
        seen = {beginWord}
        while words:
            next_words = []
            for word in words:
                if word == endWord:
                    return result
                for neighbor in adjacency_list[word]:
                    if neighbor in seen:
                        continue
                    next_words.append(neighbor)
                    seen.add(neighbor)
            words = next_words
            result += 1
        return 0

```

- ziplongest 関数
    - https://docs.python.org/3/library/itertools.html#itertools.zip_longest
- 返却する変数を result ではなく、words_and_steps の中に入れて管理するようにしてみると、幅優先探索のように考えることができて、探索中のループの中で next_nodes を管理する必要がなくなり、while 文を消せることに気づいた。
- adjacency_list という名前は何とかしたい。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
            
        def is_adjacent(word1, word2):
            differences = 0
            for c1, c2 in itertools.zip_longest(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                    return False
            return True
        
        def create_adjacency_list(wordList, beginWord):
            adjacency_list = defaultdict(list)
            for i in range(len(wordList)):
                for j in range(i + 1, len(wordList)):
                    w1 = wordList[i]
                    w2 = wordList[j]
                    if is_adjacent(w1, w2):
                        adjacency_list[w1].append(w2)
                        adjacency_list[w2].append(w1)

            if beginWord in wordList:
                return adjacency_list

            for word in wordList:
                if is_adjacent(beginWord, word):
                    adjacency_list[beginWord].append(word)
                    adjacency_list[word].append(beginWord)
            return adjacency_list

        word_to_neighbors = create_adjacency_list(wordList, beginWord)
        words_and_steps = deque([(beginWord, 1)])
        seen = {beginWord}
        while words_and_steps:
            word, step = words_and_steps.popleft()        
            if word == endWord:
                return step
            for neighbor in word_to_neighbors[word]:
                if neighbor in seen:
                    continue
                words_and_steps.append((neighbor, step + 1))
                seen.add(neighbor)
        return 0

```

- step1 で自分が書いたコードを書きかえたもの
- word_set から取り出したものは削除した方が自然な気がする。個人的には読みにくくはなっていないと思う。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
            
        def is_adjacent(word1, word2):
            differences = 0
            for c1, c2 in itertools.zip_longest(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                    return False
            return True
        
        def get_neighbors_not_seen(word_set, word):
            neighbors = []
            words_to_remove = []
            for candidate in word_set:
                if not is_adjacent(word, candidate):
                    continue
                neighbors.append(candidate)
                words_to_remove.append(candidate)
            for word in words_to_remove:
                word_set.remove(word)
            return neighbors

        word_set = set(wordList)
        words_and_steps = deque([(beginWord, 1)])
        while words_and_steps:
            word, step = words_and_steps.popleft()        
            if word == endWord:
                return step
            for neighbor in get_neighbors_not_seen(word_set, word):
                words_and_steps.append((neighbor, step + 1))
        return 0

```

- get_neighbors_not_seen 関数の中を変えたもの。こっちの方が読みやすいかな。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
            
        def is_adjacent(word1, word2):
            differences = 0
            for c1, c2 in itertools.zip_longest(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                    return False
            return True
        
        def get_neighbors_not_seen(word_set, word):
            neighbors = []
            for candidate in list(word_set):
                if not is_adjacent(word, candidate):
                    continue
                neighbors.append(candidate)
                word_set.remove(candidate)
            return neighbors

        word_set = set(wordList)
        words_and_steps = deque([(beginWord, 1)])
        while words_and_steps:
            word, step = words_and_steps.popleft()        
            if word == endWord:
                return step
            for neighbor in get_neighbors_not_seen(word_set, word):
                words_and_steps.append((neighbor, step + 1))
        return 0

```

## Step3

- word_set という変数名は個人的に好みではないみたいなので words にすると少し落ち着きましたがまだ少し気になるのでもう少し考えたい。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        def is_adjacent(word1: str, word2: str) -> bool:
            if len(word1) != len(word2):
                return False
            differences = 0
            for c1, c2 in zip(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                    return False
            return True

        def get_neighbors_not_seen(words: set[str], word: str) -> List[str]:
            neighbors = []
            for candidate in list(words):
                if not is_adjacent(word, candidate):
                    continue
                neighbors.append(candidate)
                words.remove(candidate)
            return neighbors

        words = set(wordList)
        words_and_steps = deque([(beginWord, 1)])
        while words_and_steps:
            word, step = words_and_steps.popleft()
            if word == endWord:
                return step
            for neighbor in get_neighbors_not_seen(words, word):
                words_and_steps.append((neighbor, step + 1))
        return 0

```

- wordList を、まだ発見していない単語たち、と考えることにしました。

```python

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        def is_adjacent(word1: str, word2: str) -> bool:
            if len(word1) != len(word2):
                return False
            differences = 0
            for c1, c2 in zip(word1, word2):
                if c1 == c2:
                    continue
                differences += 1
                if differences > 1:
                    return False
            return True

        def get_neighbors(words_not_seen: set[str], word: str) -> List[str]:
            neighbors = []
            for candidate in list(words_not_seen):
                if not is_adjacent(word, candidate):
                    continue
                neighbors.append(candidate)
                words_not_seen.remove(candidate)
            return neighbors

        words_not_seen = set(wordList)
        words_and_steps = deque([(beginWord, 1)])
        while words_and_steps:
            word, step = words_and_steps.popleft()
            if word == endWord:
                return step
            for neighbor in get_neighbors(words_not_seen, word):
                words_and_steps.append((neighbor, step + 1))
        return 0

```

- 今回もまだ整理できていないことがあるので復習のときにやりつつ、気持ちを切り替えてまたレビュー含めて毎日やっていこう。