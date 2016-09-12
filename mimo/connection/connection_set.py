class ConnectionSet:
    def __init__(self, connections):
        self.connections = {connection.name: connection for connection in connections}
        self.streams = {connection.name: set() for connection in connections}

    def __iter__(self):
        return iter(self.connections.values())

    def __len__(self):
        return len(self.connections)

    def __getattr__(self, key):
        if key in self.connections:
            return self.connections[key]
        return self.__getattribute__(key)

    def __getitem__(self, key):
        return self.connections[key]

    def drain(self):
        """
        Drain all connections and return the streams that received updates.
        :return: Set of updated streams
        """
        drained = set()
        for connection in self.connections.values():
            if connection.drain():
                drained.add(connection.name)
        return drained
