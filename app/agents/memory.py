class Memory:
    def __init__(self,max_messages=6):
        self.history = []
        self.max_messages = max_messages
    
    def add(self,role,message):
        self.history.append({"role":role,"content":message})
        self.history = self.history[-self.max_messages:]

    def get_context(self):
        return self.history[-6:]