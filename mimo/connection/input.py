from .connection import Connection


class Input(Connection):
    def peek(self):
        return self.entities[0]

    def pop(self):
        return self.entities.popleft()

    def extend(self, entities):
        self.entities.extend(entities)
        return len(self.entities) < self.threshold
