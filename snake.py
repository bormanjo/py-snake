import config


class FixedList(object):
    '''A list of fixed capacity'''
    def __init__(self, *args, capacity: int):
        self._data = list(args)
        self.set_capacity(capacity)

    def __repr__(self):
        return self._data.__repr__()

    def __str__(self):
        return self._data.__str__()

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return self._data.__len__()

    def __getitem__(self, i):
        return self._data[i]

    def trim(self, n: int):
        '''Return the list trimmed to capacity n'''
        if n <= 0:
            raise ValueError(f'Expected n to be >= 1, got: {n}')

        res = self._data[n:]
        self._data = self._data[:n]
        return res

    def set_capacity(self, n: int):
        '''Set the capacity of the list to n'''

        if not isinstance(n, int):
            raise ValueError(f'Expected n to be an integer, got: {type(n)}')
        if n <= 0:
            raise ValueError(f'Expected n to be >= 1, got: {n}')

        self._capacity = n

        return self.trim(n)

    def get_capacity(self):
        return self._capacity

    def add_cappacity(self, i: int):
        self.set_capacity(self._capacity + abs(i))

    def at_capacity(self):
        return self._capacity == len(self._data)

    def add(self, item):
        '''
        Add the item to the list

        Pops and returns the oldest item if at capacity (before adding item).
        Otherwise returns None
        '''
        res = self._data.pop() if self.at_capacity() else None

        self._data = [item] + self._data

        return res

    def pop(self):
        return self._data.pop()

    def first(self):
        return self._data[0]

    def last(self):
        return self._data[len(self._data)]


class Snake(object):
    def __init__(self, pos):
        self.pos = FixedList(*pos, capacity=len(pos))
        self.head_color = config.snake_head_color
        self.color = config.snake_color

    def __repr__(self):
        return self.pos.__repr__()

    def __str__(self):
        return self.pos.__str__()

    def __iter__(self):
        return self.pos.__iter__()

    def __getitem__(self, i):
        return self.__getitem__(i)

    def add(self, new_pos):
        return self.pos.add(new_pos)

    def grow(self, i: int):
        self.pos.add_cappacity(i)

    def head(self):
        return self.pos.first()

    def last(self):
        return self.pos.last()
