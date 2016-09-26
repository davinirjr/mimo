class Output:
    def __init__(self, name):
        self.name = name
        self._connections = []

    async def push(self, entity):
        for connection in self._connections:
            await connection.push(entity)

    def pipe(self, connection):
        self._connections.append(connection)

    def close(self):
        for connection in self._connections:
            connection.close()
