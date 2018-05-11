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
        print('current_state:', current_state)
        print('next_state   :', next_state)
        self.field = next_state
        self._notify_observers()

    def switch_state(self, x, y):
        if (x, y) in self._field:
            self._field.remove((x, y))
        else:
            self._field.add((x, y))
        print('model::switch_state', x, y)
        self._recompute_field_size()
        self._notify_observers()

    def get_field_at(self, x_bounds, y_bounds):
        width = x_bounds[1] - x_bounds[0]
        height = y_bounds[1] - y_bounds[0]
        rv = bitarray(width * height)
        rv.setall(False)
        for x, y in product(range(*x_bounds), range(*y_bounds)):
            rv[(x - x_bounds[0]) * width + (y - y_bounds[0])] = (x, y) in self._field
        return rv

    def _alive_neighbours(self, x, y):
        rv = []
        for i in (x - 1, x, x + 1):
            for j in (y - 1, y, y + 1):
                if (i, j) != (x, y) and (i, j) in self._field:
                    rv.append((i, j))
        return tuple(rv)

    def _recompute_field_size(self):
        try:
            print(self._field)
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
        print('bounds: ', self._x_field_bounds, self._y_field_bounds)

    def __repr__(self):
        builder = StringIO()
        for x in range(*self._x_field_bounds):
            for y in range(*self._y_field_bounds):
                if (x, y) in self._field:
                    builder.write("1")
                else:
                    builder.write("0")
            builder.write("\n")
        return builder.getvalue()

    def _notify_observers(self):
        for observer in self._observers:
            observer.model_changed()
