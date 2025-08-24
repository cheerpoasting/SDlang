from collections import deque # you can add/remove things from either end

class Dispenser:
    def __init__(self):
        self.dispenser = deque() # "double ended queue"

    # the right end (standard stack)

    def push(self, item):
        self.dispenser.append(item) # add to right end

    def pop (self):
        if len(self.dispenser) == 0:
               raise IndexError("Cannot pop from empty dispenser")
        return self.dispenser.pop()

    def peek_bottom(self, distance=1):
        if len(self.dispenser) < distance:
            raise IndexError(f"Cannot peek at distance {distance} because the dispenser isn't that large")
        peek_distance = -1 * distance # "-1" in deque means the last item
        return self.dispenser[peek_distance]

    # the left end (queue)

    def pile(self, item): # add to left end
        self.dispenser.appendleft(item)

    def grab(self):
        if len(self.dispenser) == 0:
            raise IndexError("Cannot grab from empty dispenser")
        return self.dispenser.popleft()

    def peek_top(self, distance=1):
        if len(self.dispenser) < distance:
            raise IndexError(f"Cannot peek at distance {distance} because the dispenser isn't that large")
        peek_distance = distance - 1 # avoid off by one errors
        return self.dispencer[peek_distance]
        

    
