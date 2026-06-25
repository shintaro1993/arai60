class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


def _make_key(args, kwargs):
    return args + tuple(sorted(kwargs.items()))


def my_lru_cache(user_function=None, *, max_size=128):
    if max_size < 0:
        max_size = 0

    if callable(user_function):
        return _my_lru_cache_wrapper(user_function, max_size)

    def decorating_function(func):
        return _my_lru_cache_wrapper(func, max_size)
    
    return decorating_function


def _my_lru_cache_wrapper(user_function, max_size):
    cache = {}
    head = Node()  # dummy head
    tail = Node()  # dummy tail
    head.next = tail
    tail.prev = head

    def _remove(node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(node):
        node.next = head.next
        node.prev = head
        head.next.prev = node
        head.next = node

    def wrapper(*args, **kwargs):
        key = _make_key(args, kwargs)
        node = cache.get(key)
        if node is not None:
            # cache hit
            # move accessed node to front
            _remove(node)
            _insert_front(node)
            return node.value
        # cache miss
        result = user_function(*args, **kwargs)
        if len(cache) >= max_size:
            # remove Least-recently-used node
            node_to_delete = tail.prev
            _remove(node_to_delete)
            del cache[node_to_delete.key]
        node = Node(key, result)
        _insert_front(node)
        cache[key] = node
        return result
    return wrapper


class Solution:
    def num_ways(self, n: int, k: int) -> int:
        if n < 0:
            raise ValueError("n must be a non-negative integer")
        if k < 0:
            raise ValueError("k must be a non-negative integer")  
        if n == 0 or k == 0:
            return 0
        
        @my_lru_cache
        def total_ways(num_posts):
            if num_posts == 1:
                return k
            if num_posts == 2:
                return k * k
            return (total_ways(num_posts - 1) + total_ways(num_posts - 2)) * (k - 1)
        return total_ways(n)

if __name__ == '__main__':
    s = Solution()
    assert s.num_ways(0, 2) == 0
    assert s.num_ways(1, 2) == 2
    assert s.num_ways(2, 2) == 4
    assert s.num_ways(3, 3) == 24
    assert s.num_ways(4, 3) == 66
    assert s.num_ways(30, 20) == 1004151076547626230786266566362256795580
    # assert s.num_ways(1314520, 1) == 0
