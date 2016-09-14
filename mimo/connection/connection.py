from collections import deque


class Connection:
    def __init__(self, name, threshold=10):
        self.entities = deque()

        self.name = name
        self.threshold = threshold

    def __len__(self):
        return len(self.entities)

    def is_full(self):
        return len(self.entities) >= self.threshold
