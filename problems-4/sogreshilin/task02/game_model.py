from itertools import product
from io import StringIO
from operator import itemgetter

from bitarray import bitarray


class Game:
    def __init__(self):
        self._field = set()
        self._x_field_bounds = (0, 0)
        self._y_field_bounds = (0, 0)
        self._observers = []

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        if not isinstance(value, set) or \
                not all(isinstance(x, int) and isinstance(y, int) for x, y in value):
            raise TypeError('Set of (int, int) expected')
        self._field = value
        self._recompute_field_size()

    def subscribe(self, observer):
        self._observers.append(observer)

    def next_state(self):
        current_state = self.field.copy()
        next_state = set()
        for x in range(*self._x_field_bounds):
            for y in range(*self._y_field_bounds):
                if (x, y) in current_state and 2 <= len(self._alive_neighbours(x, y)) <= 3:
                    next_state.add((x, y))
                if (x, y) not in current_state and len(self._alive_neighbours(x, y)) == 3:
                    next_state.add((x, y))
        self.field = next_state
        self._notify_observers()

    def switch_state(self, x, y):
        if (x, y) in self._field:
            self._field.remove((x, y))
        else:
            self._field.add((x, y))
        self._recompute_field_size()
        self._notify_observers()

    def _alive_neighbours(self, x, y):
        rv = []
        for i in (x - 1, x, x + 1):
            for j in (y - 1, y, y + 1):
                if (i, j) != (x, y) and (i, j) in self._field:
                    rv.append((i, j))
        return tuple(rv)

    def _recompute_field_size(self):
        try:
            min_x = min(map(itemgetter(0), self._field))
            max_x = max(map(itemgetter(0), self._field))
        except ValueError:
            min_x, max_x = 0, 0
        try:
            min_y = min(map(itemgetter(1), self._field))
            max_y = max(map(itemgetter(1), self._field))
        except ValueError:
            min_y, max_y = 0, 0
        self._x_field_bounds = (min_x - 2, max_x + 2)
        self._y_field_bounds = (min_y - 2, max_y + 2)

    def _notify_observers(self):
        for observer in self._observers:
            observer.model_changed()
