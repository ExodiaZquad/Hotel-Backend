class Queue:
    def __init__(self, lists=[]):
        self.items = lists

    def enQueue(self, item):
        self.items.append(item)

    def deQueue(self):
        if len(self.items) == 0:
            return "No queue"
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []

    def __str__(self):
        return " ".join(str(x) for x in self.items)