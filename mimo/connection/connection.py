from collections import deque


class Connection:
    def __init__(self, name, threshold=10):
        self.entities = deque()
        self.connections = set()

        self.name = name
        self.threshold = threshold

    def peek(self):
        return self.entities[0]

    def pop(self):
        return self.entities.popleft()

    def push(self, entity):
        """
        Add an entity to the end of the connection. Return if connection can still be pushed to.
        :param entity:
        :return:
        """
        self.entities.append(entity)
        return len(self.entities) < self.threshold

    def extend(self, entities):
        self.entities.extend(entities)
        return len(self.entities) < self.threshold

    def is_full(self):
        return len(self.entities) >= self.threshold

    def join(self, connection):
        self.connections.add(connection)

    def drain(self):
        entities = self.entities
        if len(entities) == 0 or any(connection.is_full() for connection in self.connections):
            return False
        for connection in self.connections:
            connection.extend(entities)
        entities.clear()
        return True
