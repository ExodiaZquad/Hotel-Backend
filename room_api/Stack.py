class Stack:
    def __init__(self, items=[]):
        self.items = items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items != []:
            return self.items.pop()
        return -1

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []