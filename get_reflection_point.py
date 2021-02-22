# import objects and functions
from Line import Line
from computation import calculate_reflection_cartesian
from output_options import write_reflection_to_csv, visualize_reflection

# current options for coordinate planes
COORDINATE_PLANE_OPTIONS = {"cartesian"}

# options for get_reflection_point()
LINE_OF_SYMMETRY_OPTIONS = {"x-axis", "y-axis"}

def get_reflection_point(points, line_of_symmetry=['x-axis'], coordinate_plane="Cartesian", rounding=None,
                         visualize=True, output_directory=None):
    '''
    reflecting given points given line(s) of symmetry, for each given point and line of symmetry

    :param points: tuple or list of tuple for points to reflect across line of symmetry
    :param line_of_symmetry: equation in which the points reflect i.e. "x-axis", "y-axis", "y=2x+3", "y=-4", "x=239"
    :param coordinate_plane: reflect points on which coordinate plane, i.e. "Cartesian"
    :param rounding: round results using Python builtin's round()
    :param visualize: option to visualize points and line of symmetry
    :param output_directory: option to output results into a directory
    :return: dictionary of line(s) of symmetry and and their reflected points
    '''

    ########################
    ### parameters check ###
    ########################

    # points can be one point or list of points for multiple points to reflect
    if isinstance(points, tuple) is False and isinstance(points, list) is False:
        raise TypeError("points %r is not a valid list." % points)

    # line_of_symmetry can be one line in string format or list of strings for multiple lines of symmetry
    if isinstance(line_of_symmetry, str) is False and isinstance(line_of_symmetry, list) is False:
        raise TypeError("lines_of_symmetry %r have invalid string instances." % line_of_symmetry)

    # coordinate plane must be the ones given
    if coordinate_plane.lower() not in COORDINATE_PLANE_OPTIONS:
        raise ValueError("coordinate_plane must be in %r." % COORDINATE_PLANE_OPTIONS)

    ################################################################################
    ### calculate: reflect n number of times based on n number of symmetry lines ###
    ################################################################################

    all_reflected_points = {}
    for input_line in line_of_symmetry:
        if isinstance(input_line, str) is False:
            raise TypeError(
                "symmetry: line of symmetry (%r) is detected as a %r. It must be a string containing %r or an equation in y-intercept (y=mx+b) form." % (
                    input_line, type(input_line), LINE_OF_SYMMETRY_OPTIONS))

        line_sym = input_line
        if input_line.lower() in LINE_OF_SYMMETRY_OPTIONS:
            if input_line.lower() == "x-axis":
                line_sym = "y=0"
            elif line_sym.lower() == "y-axis":
                line_sym = "x=0"

        # create custom Line object given equation
        line = Line(line_sym)

        # reflect all points for the current line of symmetry
        reflected_points_per_line = [calculate_reflection_cartesian(point, line, rounding) for point in points]

        # add to list of points for all symmetry lines
        all_reflected_points[line_sym] = reflected_points_per_line

    ##########################
    ### writing out output ###
    ##########################

    new_dir = None
    if output_directory:
        new_dir = write_reflection_to_csv(points, all_reflected_points, output_directory)

    if visualize:
        # get ready to pass in parameters to the visualize function
        slopes = []
        y_intercepts = []
        x_intercepts = []
        for key in all_reflected_points.keys():
            slope = Line(key).get_slope()
            y_intercept = Line(key).get_y_intercept()
            x_intercept = Line(key).get_x_intercept()
            slopes.append(slope)
            y_intercepts.append(y_intercept)
            x_intercepts.append(x_intercept)

        # pass into visualize function
        visualize_reflection(points, all_reflected_points, slopes, y_intercepts, x_intercepts, new_dir)

    return all_reflected_points
