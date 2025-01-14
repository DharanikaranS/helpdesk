class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return int(key) % self.size

    def insert(self, key, value):
        hash_key = self._hash(key)
        key_exists = False
        for i, kv in enumerate(self.table[hash_key]):
            k, v = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            self.table[hash_key][i] = (key, value)
        else:
            self.table[hash_key].append((key, value))

    def delete(self, key):
        hash_key = self._hash(key)
        for i, kv in enumerate(self.table[hash_key]):
            k, v = kv
            if key == k:
                del self.table[hash_key][i]
                return True
        return False

    def retrieve(self, key):
        hash_key = self._hash(key)
        for k, v in self.table[hash_key]:
            if k == key:
                return v
        return None

    def get_all(self):
        all_items = []
        for bucket in self.table:
            all_items.extend(bucket)
        return [item[1] for item in all_items]
