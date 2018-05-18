from operator import itemgetter


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
        next_state = set()
        x_bound_lo = float('inf')
        x_bound_hi = float('-inf')
        y_bound_lo = float('inf')
        y_bound_hi = float('-inf')
        for x in range(*self._x_field_bounds):
            for y in range(*self._y_field_bounds):
                if (x, y) in self._field and 2 <= self._alive_neighbours_count(x, y) <= 3:
                    next_state.add((x, y))
                    x_bound_lo, x_bound_hi = self.update_bounds(x, x_bound_lo, x_bound_hi)
                    y_bound_lo, y_bound_hi = self.update_bounds(y, y_bound_lo, y_bound_hi)
                if (x, y) not in self._field and self._alive_neighbours_count(x, y) == 3:
                    next_state.add((x, y))
                    x_bound_lo, x_bound_hi = self.update_bounds(x, x_bound_lo, x_bound_hi)
                    y_bound_lo, y_bound_hi = self.update_bounds(y, y_bound_lo, y_bound_hi)
        self._field = next_state
        self._x_field_bounds = (x_bound_lo - 2, x_bound_hi + 2)
        self._y_field_bounds = (y_bound_lo - 2, y_bound_hi + 2)
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

    def _alive_neighbours_count(self, x, y):
        counter = 0
        if (x - 1, y - 1) in self._field:
            counter += 1
        if (x, y - 1) in self._field:
            counter += 1
        if (x + 1, y - 1) in self._field:
            counter += 1
        if (x - 1, y) in self._field:
            counter += 1
        if (x + 1, y) in self._field:
            counter += 1
        if (x - 1, y + 1) in self._field:
            counter += 1
        if (x, y + 1) in self._field:
            counter += 1
        if (x + 1, y + 1) in self._field:
            counter += 1
        return counter

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

    def update_bounds(self, x, lo, hi):
        rv_lo = lo
        rv_hi = hi
        if x < lo:
            rv_lo = x
        elif x > hi:
            rv_hi = x
        return rv_lo, rv_hi
