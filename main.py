# import functions to find symmetry and to reflect
from get_reflection_point import get_reflection_point
from get_symmetry_line import get_symmetry_lines, find_valid_symmetry_lines
import numpy as np


if __name__ == "__main__":
    # # get line(s) of symmetry given points
    symmetry_lines_dict, lines = get_symmetry_lines([(1, -235), [34, 234], (-23, 53), (-94, -85), (3, "34"), ("3", "-345"), (-111, 234)],
                                    rounding=2, visualize=False, output_directory=r"/Users/samanthatsoi/Desktop")
    # print("lines of symmetry given points:")
    print(symmetry_lines_dict)

    # has valid line of symmetry
    symmetry_lines = find_valid_symmetry_lines([(30,2.01), (31.91,0.62), ["31.18",-1.63], (28.09,0.62), ("28.82", "-1.63")],
                                          rounding=2, visualize=True, output_directory=r"/Users/samanthatsoi/Desktop")
   # sym_lines = find_valid_symmetry_lines([(22.58,1.42), [25.42,1.42], ("22.58", "-1.42"), ["25.42", -1.42]])

    # does not have valid line of symmetry
 #   sym_lines = find_valid_symmetry_lines([(2,-9), (31.91,2), (28.09,0.62), ("28.82", "-1.63")], rounding=2, output_directory=r"/Users/samanthatsoi/Desktop")

    print("lines of symmetry given points:")
    print(symmetry_lines)

    # get reflection point given points and lines of symmetry
    output = get_reflection_point([(1, -235), [34, 234], (-23, 53)],
                                  line_of_symmetry=['y=8x-7', 'y=2x+8', 'y=-9x-220', 'x-axis', 'y-axis', 'x=2'],
                                  rounding=3, visualize=False, output_directory=r"/Users/samanthatsoi/Desktop")
    print("reflection points given lines of symmetry and given point:")
    print(output)
