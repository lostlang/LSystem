from PIL import Image, ImageDraw
import numpy
import numba
import random


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
        except TypeError:
            self._update_system()
        return self._value

    def get_value(self):
        """
        Function for get system value
        :return: value system
        """
        return self._value


def string_value_to_array(array_values, default_value):
    values = numpy.zeros((array_values.size, 2), dtype=numpy.uint)
    for i in numpy.arange(array_values.size):
        value = array_values[i].split("-")
        if value[0] == "":
            values[i][0] = default_value
            values[i][1] = default_value
            continue
        values[i][0] = value[0]
        if len(value) > 1:
            values[i][1] = value[1]
        else:
            values[i][1] = value[0]
    return values


@numba.njit(fastmath=True)
def draw_picture(actions, angles, lines,
                 stack_size, size_line,
                 start_angle, start_position):
    lines_out = numpy.zeros((lines.shape[0], 6), dtype=numpy.float64)
    stack = numpy.zeros((stack_size, 5), dtype=numpy.float64)
    stack_index = 0
    color_index = 0
    angle = start_angle
    size = size_line
    position = start_position.copy()
    index_line = 0
    index_angle = 0
    for action in actions:
        if action == 0:
            # save value
            stack[stack_index][0] = position[0]
            stack[stack_index][1] = position[1]
            stack[stack_index][2] = angle
            stack[stack_index][3] = size
            stack[stack_index][4] = color_index
            stack_index = stack_index + 1
        elif action == 4:
            # return value
            stack_index = stack_index - 1
            position[0] = stack[stack_index][0]
            position[1] = stack[stack_index][1]
            angle = stack[stack_index][2]
            size = stack[stack_index][3]
            color_index = stack[stack_index][4]
        elif action == 1:
            # add line
            line_len = numpy.random.randint(lines[index_line][0], lines[index_line][1] + 1)

            lines_out[index_line][0] = position[0]
            lines_out[index_line][1] = position[1]

            position[0] = position[0] + numpy.sin(numpy.radians(angle)) * line_len * size
            position[1] = position[1] + numpy.cos(numpy.radians(angle)) * line_len * size

            lines_out[index_line][2] = position[0]
            lines_out[index_line][3] = position[1]
            lines_out[index_line][4] = size
            lines_out[index_line][5] = color_index

            index_line = index_line + 1
        elif action == 7:
            # move
            line_len = numpy.random.randint(lines[index_line][0], lines[index_line][1] + 1)
            position[0] = position[0] + numpy.sin(numpy.radians(angle)) * line_len * size
            position[1] = position[1] + numpy.cos(numpy.radians(angle)) * line_len * size
            index_line = index_line + 1
        elif action == 3:
            # rotate left
            angle = angle + numpy.random.randint(angles[index_angle][0], angles[index_angle][1] + 1)
            index_angle = index_angle + 1
        elif action == 5:
            # rotate right
            angle = angle - numpy.random.randint(angles[index_angle][0], angles[index_angle][1] + 1)
            index_angle = index_angle + 1
        elif action == 2:
            # change color
            pass
        elif action == 6:
            # change line size
            pass
        else:
            pass
    return lines_out


class ArtistNumpy:

    action = numpy.array([
        "C",  # save system states
        "F",  # draw forward
        "I",  # change color
        "L",  # rotate left
        "P",  # return system states
        "R",  # rotate right
        "S",  # scale line size
        "f",  # move forward
        ], dtype=numpy.unicode)

    action_value = numpy.array(["I", "F", "f", "S"], dtype=numpy.unicode)
    action_rotate = numpy.array(["R", "L"], dtype=numpy.unicode)

    base_angle = "30"
    base_scale = 8

    def __init__(self,
                 start_position: [int, int],
                 start_angle: int,
                 size_canvas: (int, int),
                 back_color: str,
                 size_line: int,
                 colors: list):
        self._start_position = numpy.array(start_position)
        self._start_angle = start_angle + 90
        self._base_size_line = size_line
        self._size_line = self._base_size_line
        self._colors = colors
        self._create_canvas(size_canvas, back_color)
        self._stack_size: int

    def _create_canvas(self, size_canvas, back_color):
        if back_color in ["transparent", ""]:
            self._canvas = Image.new("RGBA", size_canvas)
        else:
            self._canvas = Image.new("RGBA", size_canvas, color=back_color)
        self._canvas_draw = ImageDraw.Draw(self._canvas)

    def restart_draw(self,
                     start_position: [int, int],
                     start_angle: int,
                     size_line: int,
                     color: list
                     ):
        pass

    def save_canvas(self, name):
        self._canvas.save(f"{name}.png")

    def _get_value_action(self, array):
        l_system_all_action = numpy.in1d(array, self.action)
        l_system_rotate_action = numpy.in1d(array, self.action_rotate)
        l_system_value_action = numpy.in1d(array, self.action_value)

        indexes_array = numpy.arange(array.size)
        indexes_action = indexes_array[l_system_all_action]

        rotate_start = indexes_array[l_system_rotate_action]
        value_start = indexes_array[l_system_value_action]

        rotate_end = indexes_action[numpy.searchsorted(indexes_action, rotate_start[:-1]) + 1]
        if rotate_start[-1] == indexes_action[-1]:
            rotate_end = numpy.append(rotate_end, array.size)
        else:
            rotate_end = numpy.append(rotate_end,
                                      indexes_action[numpy.searchsorted(indexes_action, rotate_start[-1]) + 1])

        value_end = indexes_action[numpy.searchsorted(indexes_action, value_start[:-1]) + 1]
        if value_start[-1] == indexes_action[-1]:
            value_end = numpy.add(value_end, array.size)
        else:
            value_end = numpy.append(value_end,
                                     indexes_action[numpy.searchsorted(indexes_action, value_start[-1]) + 1])

        rotate_value = numpy.array(["".join(array[n1 + 1:n2]) for n1, n2 in zip(rotate_start, rotate_end)])
        line_value = numpy.array(["".join(array[n1 + 1:n2]) for n1, n2 in zip(value_start, value_end)])

        self._angles_weight = string_value_to_array(rotate_value, self.base_angle)
        self._lines_weight = string_value_to_array(line_value, 1)

        self._actions_weight = numpy.searchsorted(self.action, array[l_system_all_action])

        self._stack_size = numpy.sum(self._actions_weight == 0)

    def read_l_system(self, l_system):
        l_system_array = numpy.array([*l_system], dtype=numpy.unicode)
        self._get_value_action(l_system_array)

    def draw(self):
        lines = draw_picture(self._actions_weight,
                             self._angles_weight,
                             self._lines_weight,
                             self._stack_size,
                             self._size_line,
                             self._start_angle,
                             self._start_position)

        for line in lines:
            self._canvas_draw.line((line[0], line[1],
                                    line[2], line[3]),
                                   width=int(line[4] / 2),
                                   fill=self._colors[int(line[5])])
