from .connection import Connection


class Output(Connection):
    def push(self, entity):
        """
        Add an entity to the end of the connection. Return if connection can still be pushed to.
        :param entity:
        :return:
        """
        self.entities.append(entity)
        return len(self.entities) < self.threshold
