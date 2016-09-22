from collections import deque


class Connection:
    def __init__(self, name, threshold=10):
        self.entities = deque()

        self.name = name
        self.threshold = threshold

    def __len__(self):
        return len(self.entities)

    def clear(self):
        self.entities.clear()

    def is_full(self):
        return len(self.entities) >= self.threshold
