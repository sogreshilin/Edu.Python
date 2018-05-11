import shutil
from tkinter import Tk, Frame, Button, LEFT, X, TOP, FLAT, RAISED, Radiobutton, IntVar, filedialog, messagebox, Canvas, \
    CENTER, BOTTOM, Scrollbar

import sys

import time

from task02.field_serializer import FieldSerializer
from task02.game_model import Game

GRID_COLOR = '#000000'
ALIVE_COLOR = '#23B334'
DEAD_COLOR = '#A2848D'
CELL_SIZE = 10
FIELD_WIDTH = 60
FIELD_HEIGHT = 40
SHIFT = 3


class Toolbar(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_buttons(self, buttons):
        for button in buttons:
            self.add_button(*button)

    def add_button(self, text, command):
        button = Button(self, text=text, command=command)
        button.pack(side=LEFT, fill=X)

    def add_radio_button_group(self, buttons, command, selected=1):
        variable = IntVar()
        variable.set(selected)

        for value, text in buttons.items():
            radio_button = Radiobutton(self, text=text, value=value, variable=variable,
                                       command=lambda: command(variable.get()), indicatoron=False)
            radio_button.pack(side=LEFT, fill=X)




class Field:
    def __init__(self, parent, model):
        self.canvas = Canvas(parent, width=SHIFT + 600, height=SHIFT + 400)
        self._draw_grid()
        self.canvas.pack()
        self.canvas.bind('<Button-1>', lambda event: self.switch_state(event.x, event.y))
        parent.bind('<Key>', lambda event: self._move_field(event))

        self.model = model
        self.model.subscribe(self)
        self.upper_left_x = 0
        self.upper_left_y = 0

    def model_changed(self):
        self._update()

    def fill_cell(self, x, y):
        print('fill_cell', x, y)
        x1, y1 = x * CELL_SIZE + SHIFT + 1, y * CELL_SIZE + SHIFT + 1
        x2, y2 = (x + 1) * CELL_SIZE + SHIFT - 1, (y + 1) * CELL_SIZE + SHIFT - 1
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=ALIVE_COLOR, fill=ALIVE_COLOR)

    def switch_state(self, x, y):
        cell_x = (x - SHIFT) // CELL_SIZE - self.upper_left_x
        cell_y = (y - SHIFT) // CELL_SIZE - self.upper_left_y
        print('view::switch_state', cell_x, cell_y)
        self.model.switch_state(cell_x, cell_y)

    def _move_field(self, event):
        print('key pressed', event.keysym)
        if event.keysym == 'Up':
            self.upper_left_y += 1
        elif event.keysym == 'Right':
            self.upper_left_x -= 1
        elif event.keysym == 'Down':
            self.upper_left_y -= 1
        elif event.keysym == 'Left':
            self.upper_left_x += 1
        print('upper left corner:', self.upper_left_x, self.upper_left_y)
        self._update()

    def _update(self):
        self.canvas.delete('all')
        self._draw_grid()
        self._fill_cells()

    def _draw_grid(self):
        self.canvas.create_line(3, 3, 600, 3, fill='red')
        for x in range(SHIFT, (FIELD_WIDTH + 1) * CELL_SIZE + SHIFT, CELL_SIZE):
            self.canvas.create_line(x, SHIFT, x, FIELD_HEIGHT * CELL_SIZE + SHIFT, fill=GRID_COLOR)
        for y in range(SHIFT, (FIELD_HEIGHT + 1) * CELL_SIZE + SHIFT, CELL_SIZE):
            self.canvas.create_line(SHIFT, y, FIELD_WIDTH * CELL_SIZE + SHIFT, y, fill=GRID_COLOR)

    def _fill_cells(self):
        for x in range(-self.upper_left_x, -self.upper_left_x + FIELD_WIDTH):
            for y in range(-self.upper_left_y, -self.upper_left_y + FIELD_HEIGHT):
                if (x, y) in self.model.field:
                    print(f'({x}, {y})')
                    self.fill_cell(x + self.upper_left_x, y + self.upper_left_y)


class GameApp:
    def __init__(self):
        self.model = Game()
        self.job = None
        self.speed = 1
        self.root = Tk()
        self.toolbar = Toolbar(self.root)
        self.toolbar.add_buttons((('Load', self.load), ('Save', self.save),
                                  ('Play', self.play), ('Pause', self.pause)))
        self.toolbar.add_radio_button_group(buttons={1: 'x1', 2: 'x2', 4: 'x4', 8: 'x8', 16: 'x16', 32: 'x32'},
                                            command=self.on_speed_changed)
        self.toolbar.pack(side=TOP, fill=X)
        self.canvas = Field(self.root, self.model)
        self.root.resizable(False, False)

    def load(self):
        filename = filedialog.askopenfilename(initialdir="./data/", title="Select file",
                                              filetypes=(("Life files", "*.life"), ("All files", "*.*")))
        try:
            with open(filename, 'r') as file:
                field = FieldSerializer.deserialize(file)
                self.model.field = field
        except IOError as error:
            messagebox.showerror('Error', 'Invalid file')
            print(error, file=sys.stderr)

    def save(self):
        filename = filedialog.asksaveasfilename(initialdir="./data/", title="Save file as",
                                                filetypes=(("Life files", "*.life"), ("All files", "*.*")))
        try:
            with open(filename, 'w') as file:
                buffer = FieldSerializer.serialize(self.model.field)
                buffer.seek(0)
                shutil.copyfileobj(buffer, file)
                buffer.close()
        except IOError as error:
            messagebox.showerror('Error', 'File was not saved')
            print(error, file=sys.stderr)

    def play(self):
        now = time.strftime("%H:%M:%S")
        print(now)
        self.model.next_state()
        self.job = self.root.after(int(self.speed * 1000), self.play)

    def pause(self):
        if self.job:
            self.root.after_cancel(self.job)

    def on_speed_changed(self, value):
        self.speed = 1 / value

    def switch_state(self, x, y):
        print(x, y)


if __name__ == '__main__':
    GameApp().root.mainloop()
