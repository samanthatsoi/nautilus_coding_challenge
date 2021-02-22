from Line import Line

def calculate_symmetry_cartesian(point1, point2):
    '''
    get a line of symmetry given two points

    steps to find line of symmetry
    1. find midpoint between two points
    2. find line that make up the two points
    3. find the perpendicular slope for that line
    4. find perpendicular line that goes through the midpoint

    :param point1: tuple or list of one point (x, y), i.e. (23,-45.67)
    :param point2: tuple or list of one point (x, y), i.e. (25,-45.67)
    :return: dictionary representing line of symmetry, i.e. {((23,-45.67), (25,-45.67)): "x=24"}
    '''

    # step 1. find midpoint between two points
    midpoint = get_midpoint(point1, point2)

    # step 2. find line that make up the two points
    line = get_line(point1, point2)

    # step 3. find the perpendicular slope for that line
    perpendicular_m = get_perpendicular_slope(line.get_slope())

    # step 4. find perpendicular line that goes through the midpoint
    line_of_sym = point_slope(midpoint, perpendicular_m)

    return line_of_sym


def calculate_reflection_cartesian(point, line_of_symmetry, rounding=None):
    '''
    reflect a point over a line

    #steps to reflect
    1. get line perpendicular to line of symmetry that passes given point
    2. get point where the line of symmetry and perpendicular line intersect
    3. find new point equidistant from given point to intersection point along the perpendicular line
    a.k.a. intersection point is the midpoint between reflected  point and given point

    :param point: point to reflect
    :param line_of_symmetry: Line object, the line to reflect the point over
    :param rounding: round resulting points to # of decimal place using python builtin round()
    :return: reflected point
    '''

    # step 1. get line perpendicular to line of symmetry
    perpendicular_m = get_perpendicular_slope(line_of_symmetry.get_slope())
    perpendicular_line = point_slope(point, perpendicular_m)

    # step 2. get point where the line of symmetry and perpendicular line intersect
    midpoint = get_intersection_point(line_of_symmetry, perpendicular_line)

    # step 3. find new point equidistant from given point to intersection point along the perpendicular line
    reflected_point = get_endpoint(point, midpoint)

    output_point = reflected_point

    # if a rounding decimal number is provided
    if rounding:
        output_point = tuple([round(p, rounding) for p in reflected_point])

    return output_point


def get_midpoint(point1, point2):
    '''
    get midpoint using midpoint formula given two points
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    :param point1: tuple or list of one point (x, y), i.e. (23,-45.67)
    :param point2: tuple or list of one point (x, y), i.e. (25,-45.67)
    :return: tuple representing midpoint (x,y), i.e. (23,-45.67)
    '''

    ########################
    ### parameters check ###
    ########################
    if isinstance(point1, tuple) is False and isinstance(point1, list) is False:
        raise TypeError("get_midpoint: input point %r must be a tuple or a list." % point2)

    if len(point1) < 2:
        raise ValueError("get_midpoint: point {} must be a valid point in 2D plane, i.e. (x,y)".format(point1))
    # get point
    try:
        x1 = float(point1[0])
        y1 = float(point1[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_midpoint: point %r cannot be found!" % point1
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    # parameter error check
    if isinstance(point2, tuple) is False and isinstance(point2, list) is False:
        raise TypeError("get_midpoint: input point %r must be a tuple or a list." % point2)

    if len(point1) < 2:
        raise ValueError("get_midpoint: point {} must be a valid point in 2D plane, i.e. (x,y)".format(point2))
    # get point
    try:
        x2 = float(point2[0])
        y2 = float(point2[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_midpoint: point %r cannot be found!" % point2
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    #################
    ### calculate ###
    #################
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2

    return (midpoint_x, midpoint_y)


def get_perpendicular_slope(slope):
    '''
    calculate perpendicular slope given slope

    :param slope: number representing slope, or "DNE" if slope does not exist.
    :return: float representing the perpendicular slope. "DNE" if perpendicular slope does not exist.
    '''

    perpendicular_m = 0.0

    ########################
    ### parameters check ###
    ########################
    # if line is vertical, then perpendicular slope is 0.
    if slope == "DNE":
        pass
    else:
        ### parameter check
        try:
            m = float(slope)
        except ValueError as e:
            # reraise it with custom message
            error_msg_output = "get_perpendicular_slope: input slope is invalid!"
            print(error_msg_output)
            e.args += (error_msg_output,)
            raise

        #################
        ### calculate ###
        #################

        perpendicular_m = "DNE"
        # if line is horizontal, perpendicular slope does not exist.
        if m == 0:
            pass
        else:
            perpendicular_m = -1 / m

    return perpendicular_m


def get_line(point1, point2):
    '''
    get line given two points using slope-intercept

    :param point1: tuple or list of one point (x, y), i.e. (23,-45.67)
    :param point2: tuple or list of one point (x, y), i.e. (25,-45.67)
    :return: Line object representing line between point1 and point2
    '''
    ########################
    ### parameters check ###
    ########################

    if isinstance(point1, tuple) is False and isinstance(point1, list) is False:
        raise TypeError("get_line: input point %r must be a tuple or a list." % point2)

    if len(point1) < 2:
        raise ValueError("get_line: point {} must be a valid point in 2D plane, i.e. (x,y)".format(point1))
    # get point
    try:
        x1 = float(point1[0])
        y1 = float(point1[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_line: point %r cannot be found!" % point1
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    # parameter error check
    if isinstance(point2, tuple) is False and isinstance(point2, list) is False:
        raise TypeError("get_line: input point %r must be a tuple or a list." % point2)

    if len(point1) < 2:
        raise ValueError("get_line: point {} must be a valid point in 2D plane, i.e. (x,y)".format(point2))
    # get point
    try:
        x2 = float(point2[0])
        y2 = float(point2[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_line: point %r cannot be found!" % point2
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    #################
    ### calculate ###
    #################

    slope_intercept_eq = ""
    if (x1 - x2 == 0):
        slope_intercept_eq = "x=%s" % x1
    else:
        # y = mx+b
        # get m
        m = (y1 - y2) / (x1 - x2)
        # get b
        b = (x1 * y2 - x2 * y1) / (x1 - x2)

        # put in string format. if negative, string does not need a '+'
        if (b >= 0):
            slope_intercept_eq = "y=%sx+%s" % (m, b)
        else:
            slope_intercept_eq = "y=%sx%s" % (m, b)

    return Line(slope_intercept_eq)


def point_slope(point, slope):
    '''
    creates a Line object given a point and slope using point-slope formula
    point slope: y - y1 = m(x - x1)
    i.e. y - 2 = (1/2)(x - 5) -> y = y = (1/2)x - (5*(1/2) + 2)

    :param point: a tuple (x, y) or a list [x, y]
    :param slope: a digit representing the slope
    :return: Line object
    '''

    ########################
    ### parameters check ###
    ########################

    if isinstance(point, tuple) is False and isinstance(point, list) is False:
        raise TypeError("point_slope: input point %r must be a tuple or a list." % point)

    # get point
    try:
        x = float(point[0])
        y = float(point[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "point_slope: point %r cannot be found!" % point
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    #################
    ### calculate ###
    #################

    # it is a straight line of slope does not exist, i.e. x=-2
    if slope == "DNE":
        slope_intercept_eq = "x=%s" % x
    else:
        # parameter check
        try:
            m = float(slope)
        except ValueError as e:
            error_msg_output = "point_slope: input slope %r is invalid!" % slope
            print(error_msg_output)
            e.args += (error_msg_output,)
            raise

        # put in y-intercept form to put get a Line object
        b = (-x * m) + y
        # put in string format. if negative, string does not need a '+'
        if (b >= 0):
            slope_intercept_eq = "y=%sx+%s" % (m, b)
        else:
            slope_intercept_eq = "y=%sx%s" % (m, b)

    return Line(slope_intercept_eq)


def get_intersection_point(line1, line2):
    '''
    find the point where two lines intersect

    setting their slope intercept form to each other
    i.e. step 1. line1) y = 2x line2) y=-4x+9
    step 2. 2x = -4x+9
    step 3. find x
    step 4. plug in x in either eq. to find y

    :param line1: Line object
    :param line2: Line object
    :return: tuple (x,y), intersection point. "DNE" if there is no point of intersection
    '''
    ########################
    ### parameters check ###
    ########################

    if isinstance(line1, Line) is False or isinstance(line2, Line) is False:
        raise TypeError("get_intersection_point: input line parameters must be Line objects.")

    #################
    ### calculate ###
    #################
    # get line information
    line1_m = line1.get_slope()
    line1_b = line1.get_y_intercept()

    line2_m = line2.get_slope()
    line2_b = line2.get_y_intercept()

    if (line1_m == "DNE" and line1_b == "DNE"):
        # line 1 is vertical, so intersection point x must be where x-axis intercepts line 1
        x = line1.get_x_intercept()

        # plug x in to find y
        y = (line2_m * x) + line2_b

    elif (line2_m == "DNE" and line2_b == "DNE"):
        # line 2 is vertical, so intersection point x must be where x-axis intercepts line 2
        x = line2.get_x_intercept()
        y = line1_m * x + line1_b

    else:
        # find x by putting constants in one side and x on the other
        left_m = line1_m - line2_m
        right_b = line2_b - line1_b

        # isolate x
        try:
            x = right_b / left_m
        except ZeroDivisionError as e:
            # reraise it with custom message
            error_msg_output = "get_intersection_point: cannot find intersection points for %s and %s!" % \
                               (line1.equation, line2.equation)
            print(error_msg_output)
            e.args += (error_msg_output,)
            raise

        # plug x back in line 1 or line 2 to find y
        y = line1_m * x + line1_b

    return (x, y)


def get_endpoint(point, midpoint):
    '''
    find new point, a.k.a. "endpoint", equidistant from given point to another point, a.k.a. "midpoint"

    midpoint formula: (midpoint_x = (x1 + x2) / 2, midpoint_y = (y1 + y2) / 2)
    i.e. (2 = (x1 + 4) / 2, 7 = (y1 - 5) / 2)

    :param point: a tuple (x, y) as the starting point
    :param midpoint: a tuple (x, y) as the midpoint to reflect the starting point over
    :return: a tuple (x, y), "endpoint"
    '''

    ########################
    ### parameters check ###
    ########################
    # making sure point passed in can be translated to (x, y)
    if isinstance(point, tuple) is False and isinstance(point, list) is False:
        raise TypeError("get_endpoint: input point %r must be a tuple or a list!" % point)

    # input parameter check
    try:
        point_x = float(point[0])
        point_y = float(point[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_endpoint: input point %r cannot be found!" % point
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    # making sure midpoint passed in can be translated to (x, y)
    if isinstance(midpoint, tuple) is False and isinstance(midpoint, list) is False:
        raise TypeError("get_endpoint: input midpoint %r must be a tuple or a list!" % midpoint)

    # input parameter check
    try:
        midpoint_x = float(midpoint[0])
        midpoint_y = float(midpoint[1])
    except ValueError as e:
        # reraise it with custom message
        error_msg_output = "get_endpoint: midpoint %r cannot be found!" % midpoint
        print(error_msg_output)
        e.args += (error_msg_output,)
        raise

    #################
    ### calculate ###
    #################

    # apply midpoint formula to find endpoint (x,y)
    x = (midpoint_x * 2) - point_x
    y = (midpoint_y * 2) - point_y

    return (x, y)
