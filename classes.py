import random
from PIL import Image, ImageDraw
import math


class LSystem:
    def __init__(self,
                 seed: str,
                 rules: dict):
        """
        Create object LSystem type
        :param seed: start system value
        :param rules: rule for changing system
        """
        self._value = seed
        self._rules = rules

    def _update_system(self):
        """
        Function for updating system value
        """
        self._value = "".join([self._rules[i] if i in self._rules else i
                               for i in self._value])

    def next(self,
             step=None):
        """
        Function for use rules into system value
        :param step: number of iteration ( if type not int, step = 1 )
        :return: value system after step
        """
        try:
            for i in range(step):
                self._update_system()
        except:
            self._update_system()
        return self._value

    def get_value(self):
        """
        Function for get system value
        :return: value system
        """
        return self._value


class Artist:

    action = ["R",   # rotate right
              "L",   # rotate left
              "I",   # change color
              "C",   # save system states
              "P",   # return system states
              "F",   # draw forward
              "f",   # move forward
              "S"]   # scale line size

    action_with_value = ["R", "L", "I", "F", "f", "S"]

    base_angle = "30"
    base_scale = 8

    stack = []

    def __init__(self,
                 start_position: [int, int],
                 start_angle: int,
                 size_canvas: (int, int),
                 back_color: str,
                 size_line: int,
                 color: list):
        """
        Create object Artist type
        :param start_position: x and y point to start image
        :param size_canvas: height and width image
        :param back_color: color for background image, if value "transparent" or "" create image with transparent
         background
        :param size_line: start size line
        :param color: list of color for drawing
        """
        self._position = start_position
        self._angle = start_angle + 90
        self._base_size_line = size_line
        self._size_line = self._base_size_line
        self._color = color
        self._select_color = 0
        self._create_canvas(size_canvas, back_color)

    def _create_canvas(self, size_canvas, back_color):
        if back_color in ["transparent", ""]:
            self._canvas = Image.new("RGBA", size_canvas)
        else:
            self._canvas = Image.new("RGBA", size_canvas, color=back_color)
        self._canvas_draw = ImageDraw.Draw(self._canvas)

    def _push(self):
        self.stack.append(
            [[*self._position],
             self._angle,
             self._size_line,
             self._select_color]
        )

    def _pop(self):
        self._position = self.stack[-1][0]
        self._angle = self.stack[-1][1]
        self._size_line = self.stack[-1][2]
        self._select_color = self.stack[-1][3]
        self.stack.pop()

    def _rotate(self, side, angle):
        rate = 1 if side == "L" else -1
        if type(angle) is list:
            angle = random.randint(*angle)
        elif not angle:
            angle = self.base_angle
        self._angle += angle * rate

    def _scale(self, value):
        if type(value) is list:
            value = (random.random() * (value[-1]-value[0]) + value[0]) / pow(10, len(str(value[-1])))
        elif value:
            value = value / pow(10, len(str(value)))
        else:
            value = self.base_scale / 10
        self._size_line *= value

    def _change_color(self, value):
        if not value:
            value = 1
        self._color += value

    def _move(self, value):
        if type(value) is list:
            value = random.randint(*value)
        elif not value:
            value = self._size_line
        self._position = [
            self._position[0] + math.sin(math.radians(self._angle)) * value,
            self._position[1] + math.cos(math.radians(self._angle)) * value
        ]
        return self._position

    def _draw(self, value):
        if type(value) is list:
            value = random.randint(*value)
        elif not value:
            value = self._size_line
        self._canvas_draw.line((*self._position,
                                *self._move(value)),
                               width=self._base_size_line,
                               fill=self._color[self._select_color])

    def restart_draw(self,
                     start_position: [int, int],
                     start_angle: int,
                     size_line: int,
                     color: list
                     ):
        self._position = start_position
        self._angle = start_angle + 90
        self._base_size_line = size_line
        self._color = color
        self._select_color = 0
        self._size_line = self._base_size_line

    def save_canvas(self, name):
        self._canvas.save(f"{name}.png")

    def read_l_system(self, l_system):
        index_to_l_system_string = 0

        while True:
            try:
                action = l_system[index_to_l_system_string]
                value_action = ""
            except IndexError:
                break
            if action in self.action_with_value:
                index_to_l_system_string += 1
                try:
                    while l_system[index_to_l_system_string] not in self.action:
                        value_action += l_system[index_to_l_system_string]
                        index_to_l_system_string += 1
                except IndexError:
                    pass
                if "~" in value_action:
                    value_action = list(map(int, value_action.split("~")))
                elif value_action:
                    value_action = int(value_action)
            else:
                index_to_l_system_string += 1

            if action == "C":
                self._push()
            elif action == "P":
                self._pop()
            elif action in ["R", "L"]:
                self._rotate(action, value_action)
            elif action == "F":
                self._draw(value_action)
            elif action == "f":
                self._move(value_action)
            elif action == "S":
                self._scale(value_action)
            elif action == "I":
                self._change_color(value_action)
            else:
                pass
