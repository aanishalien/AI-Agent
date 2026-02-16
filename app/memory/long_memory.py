class LongTermMemory:
    def __init__(self):
        self.facts = []

    def remeber(self, fact):
        self.facts.append(fact)
        print("\n[LTM STORED]")
        print(self.facts)

    def recall(self):
        return "\n".join(self.facts)