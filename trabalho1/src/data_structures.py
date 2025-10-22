from typing import List

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
        raise IndexError("pop from empty stack")

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

class Queue:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            # Operação O(n) para garantir o FIFO sem usar collections.deque
            return self._items.pop(0) 
        raise IndexError("pop from empty queue")

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

class PriorityQueue:

    def __init__(self):
        self._items = []
        self._counter = 0

    def push(self, priority: float, item):
        entry = (priority, self._counter, item)
        self._counter += 1
        
        # Inserção que mantém a lista ordenada por prioridade (O(n))
        i = 0
        while i < len(self._items) and self._items[i][0] <= priority:
            i += 1
            
        self._items.insert(i, entry)

    def pop(self):
        if not self.is_empty():
            priority, count, item = self._items.pop(0)
            return item
        raise IndexError("pop from empty priority queue")

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)
