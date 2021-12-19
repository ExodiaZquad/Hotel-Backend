class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items != []:
            self.items.pop()

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []