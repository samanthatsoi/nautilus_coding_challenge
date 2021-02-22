# import objects and functions
from Line import Line
from computation import calculate_symmetry_cartesian
from output_options import write_symmetry_to_csv, visualize_symmetry


# current options for coordinate planes
COORDINATE_PLANE_OPTIONS = {"cartesian"}


def get_symmetry_line(points, coordinate_plane="Cartesian", rounding=4, visualize=True, output_directory=None):
    '''
    get line(s) of symmetry given list of points, fo each given set of points

    :param points: list of tuples or list that represent points to get line of symmetry
    :param coordinate_plane: reflect points on which coordinate plane, i.e. "Cartesian"
    :param rounding: round results using Python builtin's round()
    :param visualize: option to visualize points and line of symmetry
    :param output_directory: option to output results into a directory
    :return: dictionary of given points and resulting line(s) of symmetry
    '''

    ########################
    ### parameters check ###
    ########################

    # points can be one point or list of points for multiple points to reflect
    if isinstance(points, list) is False:
        raise TypeError("get_symmetry_line: points {} must be a valid list.".format(points))

    if len(points) < 2:
        raise ValueError(
            "get_symmetry_line: points {}, there must be at least 2 points as input to find the line of symmetry".format(
                points))

    # check if points passed in are valid points
    if all(isinstance(p, (tuple, list)) and len(p) == 2 for p in points) is False:
        raise TypeError(
            "get_symmetry_line: points {} must include valid 2D points in a tuple or a list, i.e. (2,5) or [-352.54,-2343.5]".format(
                points))

    # check that each point is a int, float, or a str that is a digit
    p_components = [p_component for p in points for p_component in p if ((isinstance(p_component, (int, float)) or (
            isinstance(p_component, str) and p_component.isdigit())) is False)]
    # could also be a float
    for p_comp in p_components:
        try:
            float(p_comp)
        except ValueError as e:
            # reraise it with custom message
            error_msg_output = "get_symmetry_line: {} is not a valid digit!".format(p_comp)
            print(error_msg_output)
            e.args += (error_msg_output,)
            raise

    # coordinate plane must be the ones given
    if coordinate_plane.lower() not in COORDINATE_PLANE_OPTIONS:
        raise ValueError("get_symmetry_line: coordinate_plane must be in {}.".format(COORDINATE_PLANE_OPTIONS))

    ########################################################
    ### calculate: get a line of symmetry for each point ###
    ########################################################

    lines_of_symmetry = {}
    for point_i in range(len(points)):
        next_i = point_i + 1
        for point_j in range(next_i, len(points)):
            # get ready to pass into calulating function
            point1 = tuple(points[point_i])
            point2 = tuple(points[point_j])

            # calculate
            line_of_symmetry = calculate_symmetry_cartesian(point1, point2)

            # what to output
            line_of_symmetry_output = line_of_symmetry.equation

            # rounding result
            if rounding:
                b = line_of_symmetry.get_y_intercept()
                m = line_of_symmetry.get_slope()
                # put in string format. if negative, string does not need a '+'
                if (b == "DNE" or m == "DNE"):
                    line_of_symmetry_output = "x=%s" % line_of_symmetry.get_x_intercept()
                else:
                    b_round = round(b, rounding)
                    m_round = round(m, rounding)
                    if (b >= 0):
                        line_of_symmetry_output = "y=%sx+%s" % (m_round, b_round)
                    else:
                        line_of_symmetry_output = "y=%sx%s" % (m_round, b_round)

            # add to data structure with all lines
            lines_of_symmetry[(point1, point2)] = line_of_symmetry_output

    ##########################
    ### writing out output ###
    ##########################

    new_dir = None
    # do we want to write out CSV file?
    if output_directory:
        new_dir = write_symmetry_to_csv(lines_of_symmetry, output_directory)

    # do we want to visualize?
    if visualize:
        # get ready to pass in parameters to the visualize function
        slopes = []
        y_intercepts = []
        x_intercepts = []
        for line in lines_of_symmetry.values():
            slope = Line(line).get_slope()
            y_intercept = Line(line).get_y_intercept()
            x_intercept = Line(line).get_x_intercept()
            slopes.append(slope)
            y_intercepts.append(y_intercept)
            x_intercepts.append(x_intercept)

        # pass into visualize function
        visualize_symmetry(lines_of_symmetry, slopes, y_intercepts, x_intercepts, new_dir)

    return lines_of_symmetry
