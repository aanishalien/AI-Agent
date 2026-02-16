class ShortTermMemory:
    def __init__(self,limit=5):
        self.limit = limit
        self.history = []

    def add(self,role,content):
        self.history.append({"role": role,"content":content})
        if len(self.history) > self.limit:
            self.history.pop(0)

    def get_context(self):
        return self.history