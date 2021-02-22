# import functions to find symmetry and to reflect
from get_reflection_point import get_reflection_point
from get_symmetry_line import get_symmetry_line


if __name__ == "__main__":
    # get line(s) of symmetry given points
    sym_lines = get_symmetry_line([(1, -235), [34, 234], (-23, 53), (-94, -85), (3, "34"), ("3", "-345"), (-111, 234)],
                                  rounding=2, visualize=True, output_directory=r"/Users/samanthatsoi/Desktop")
    print("lines of symmetry given points:")
    print(sym_lines)

    # get reflection point given points and lines of symmetry
    output = get_reflection_point([(1, -235), [34, 234], (-23, 53)],
                                  line_of_symmetry=['y=8x-7', 'y=2x+8', 'y=-9x-220', 'x-axis', 'y-axis', 'x=2'],
                                  rounding=3, visualize=True, output_directory=r"/Users/samanthatsoi/Desktop")
    print("reflection points given lines of symmetry and given point:")
    print(output)
