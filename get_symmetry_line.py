# import objects and functions
from Line import Line
from computation import calculate_symmetry_cartesian, calculate_reflection_cartesian
from output_options import write_symmetry_to_csv, visualize_symmetry, visualize_valid_lines, write_valid_lines_csv
from math import floor, ceil

# current options for coordinate planes
COORDINATE_PLANE_OPTIONS = {"cartesian"}


def find_valid_symmetry_lines(points, coordinate_plane="Cartesian", rounding=3, visualize=True, output_directory=None):
    '''
    find valid lines of symmetry that correspond with the entire set of input points.

    procedure:
    1. find all lines of symmetry given each pair of points in the input set
    2. for each line found, if the rest of the points have a corresponding reflection point (or is on the line),
    then it is a valid line of symmetry

    :param points: list of tuples or list that represent points to get line of symmetry
    :param coordinate_plane: reflect points on which coordinate plane, i.e. "Cartesian"
    :param rounding: round output results using Python builtin's round()
    :param visualize: option to visualize points and line of symmetry
    :param output_directory: option to output results into a directory
    :return: list of equations of valid lines of symmetry. empty list if none found.
    '''

    # get all lines of symmetry first, error checking happens in get_symmetry_lines
    output_dict, lines_of_symmetry = get_symmetry_line(points, coordinate_plane, visualize=False)

    ########################################################
    ### calculate valid line of symmetry ###################
    ########################################################

    # prepare, get rounded number of the input points to account for rounding errors for comparison
    t_points = [tuple(t_point) for t_point in points]
    points_float = [(float(p[0]), float(p[1])) for p in t_points]
    points_round = [(round(p_float[0], 2), round(p_float[1], 2)) for p_float in points_float]

    # holds output
    valid_lines_of_sym = []
    valid_line_eqs = []

    # iterate each symmetry line found for each pair of points to see if other points reflect across it
    # if all input points have a corresponding reflection, then it is a valid symmetry line
    for line in lines_of_symmetry:
        valid = []

        no_point_combination = 0
        for point in points:
            # get the reflected point. if input point is on the line, then reflected point will be the same point
            reflected_point = calculate_reflection_cartesian(point, line)

            # get floor and ceiling of the calculated point up to 2 decimal places, so we can account rounding error
            # reference for calculating floor and ceiling up to decimal places:
            # https://stackoverflow.com/questions/50405017/how-to-round-up-a-number-to-x-decimal-places-in-python
            floor_x = floor(reflected_point[0] * 100) / 100
            floor_y = floor(reflected_point[1] * 100) / 100
            ceil_x = ceil(reflected_point[0] * 100) / 100
            ceil_y = ceil(reflected_point[1] * 100) / 100

            # if reflected point is also an input
            if reflected_point in points_round \
                    or (floor_x, floor_y) in points_round or (ceil_x, ceil_y) in points_round \
                    or (floor_x, ceil_y) in points_round or (ceil_x, floor_y) in points_round:
                valid.append(True)
            no_point_combination += 1

        # if all points found a reflected point, then this is a valid line of symmetry
        if (len(valid) == no_point_combination):
            if line.equation not in valid_line_eqs:
                valid_lines_of_sym.append(line)
                valid_line_eqs.append(line.equation)

    ########################################################
    ### ROUNDING RESULTS ###################################
    ########################################################
    if rounding:
        valid_line_eqs_round = []
        for line_of_symmetry in valid_lines_of_sym:
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
            valid_line_eqs_round.append(line_of_symmetry_output)
        valid_line_eqs = valid_line_eqs_round



    ########################################################
    ### PLOTTING POINTS AND LINES ##########################
    ########################################################
    new_dir = None
    # do we want to write out CSV file?
    if output_directory:
        new_dir = write_valid_lines_csv(points, valid_line_eqs, output_directory)
    if visualize:
        #prepare to pass into function
        slopes = [line.get_slope() for line in valid_lines_of_sym]
        y_intercepts = [line.get_y_intercept() for line in valid_lines_of_sym]
        x_intercepts = [line.get_x_intercept() for line in valid_lines_of_sym]

        visualize_valid_lines(points_round, valid_line_eqs, slopes, y_intercepts, x_intercepts, new_dir)

    return valid_line_eqs


def get_symmetry_line(points, coordinate_plane="Cartesian", rounding=4, visualize=True, output_directory=None):
    '''
    get line(s) of symmetry given list of points, fo each given set of points

    :param points: list of tuples or list that represent points to get line of symmetry
    :param coordinate_plane: reflect points on which coordinate plane, i.e. "Cartesian"
    :param rounding: round results using Python builtin's round()
    :param visualize: option to visualize points and line of symmetry
    :param output_directory: option to output results into a directory
    :return: dictionary of given points and their resulting line(s) of symmetry,
        list of Line objects of symmetry lines found
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

    lines_of_symmetry_dict = {}
    all_lines_of_sym = []
    for point_i in range(len(points)):
        next_i = point_i + 1
        for point_j in range(next_i, len(points)):
            # get ready to pass into calulating function
            point1 = tuple(points[point_i])
            point2 = tuple(points[point_j])

            # calculate
            line_of_symmetry = calculate_symmetry_cartesian(point1, point2)

            all_lines_of_sym.append(line_of_symmetry)
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
            lines_of_symmetry_dict[(point1, point2)] = line_of_symmetry_output

    ##########################
    ### writing out output ###
    ##########################

    new_dir = None
    # do we want to write out CSV file?
    if output_directory:
        new_dir = write_symmetry_to_csv(lines_of_symmetry_dict, output_directory)

    # do we want to visualize?
    if visualize:
        # get ready to pass in parameters to the visualize function
        slopes = []
        y_intercepts = []
        x_intercepts = []
        for line in lines_of_symmetry_dict.values():
            slope = Line(line).get_slope()
            y_intercept = Line(line).get_y_intercept()
            x_intercept = Line(line).get_x_intercept()
            slopes.append(slope)
            y_intercepts.append(y_intercept)
            x_intercepts.append(x_intercept)

        # pass into visualize function
        visualize_symmetry(lines_of_symmetry_dict, slopes, y_intercepts, x_intercepts, new_dir)

    return lines_of_symmetry_dict, all_lines_of_sym
