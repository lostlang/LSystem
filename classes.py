from PIL import Image, ImageDraw
import numpy
import numba


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


class ArtistNumpy:

    action = numpy.array(["R",  # rotate right
                          "L",  # rotate left
                          "I",  # change color
                          "C",  # save system states
                          "P",  # return system states
                          "F",  # draw forward
                          "f",  # move forward
                          "S"], dtype=numpy.unicode)    # scale line size

    action_value = numpy.array(["I", "F", "f", "S"], dtype=numpy.unicode)
    action_rotate = numpy.array(["R", "L"], dtype=numpy.unicode)

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
        pass

    def _pop(self):
        pass

    def _rotate(self, side, angle):
        pass

    def _scale(self, value):
        pass

    def _change_color(self, value):
        pass

    def _move(self, value):
        pass

    def _draw(self, value):
        pass

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
            rotate_end = numpy.append(rotate_end, rotate_start[-1])

        value_end = indexes_action[numpy.searchsorted(indexes_action, value_start[:-1]) + 1]
        if value_start[-1] == indexes_action[-1]:
            value_end = numpy.add(value_end, [array.size])
        else:
            value_end = numpy.append(value_end, value_start[-1])

        rotate_value = numpy.array(["".join(array[n1 + 1:n2]) for n1, n2 in zip(rotate_start, rotate_end)])
        painting_value = numpy.array(["".join(array[n1 + 1:n2]) for n1, n2 in zip(value_start, value_end)])

        print(rotate_value)
        print(painting_value)


        # rotate_value = get_value(array, rotate_start, rotate_end)
        # painting_value = get_value(array, value_start, value_end)

        # print(rotate_value)



    def read_l_system(self, l_system):
        l_system_array = numpy.array([*l_system], dtype=numpy.unicode)
        self._get_value_action(l_system_array)

    pass
