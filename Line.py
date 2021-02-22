class Line(object):
    """
    A class used to represent a Line given an equation in slope-intercept form, x=x1, or y=y1, i.e. y=3x-231.4, x=2, y=-34421.6

    ...

    Attributes
    ----------
    equation : str
        a formatted string to print out what the line is in slope-intercept form, i.e. y=3x-231.4, x=2, y=-34421.6

    Methods
    -------
    get_slope()
        calculate slope of given line

    get_y_intercept()
        calculate the y intercept of given line

    get_x_intercept()
        calculate the x intercept of given line
    """

    def __init__(self, slope_intercept_eq):
        ########################
        ### parameters check ###
        ########################

        if isinstance(slope_intercept_eq, str) is False:
            raise TypeError("Line: equation inputted %r must be a string.", slope_intercept_eq)

        # make sure it is in valid slope intercept form. error if string does not have a '=',
        # starts or ends with '=', a 'x' or 'y', if 'y' is found after '=',
        # if it does not start with a x= or y=
        if ((slope_intercept_eq.find("=") <= 0) or
                (slope_intercept_eq.find("=") == len(slope_intercept_eq) - 1) or
                # there must be x or y in the equation
                (slope_intercept_eq.find("y") < 0 and slope_intercept_eq.find("x") < 0) or
                # "y" cannot be found after "="
                (slope_intercept_eq.find("y") >= 0 and slope_intercept_eq.find("y") > slope_intercept_eq.find("=")) or
                # making sure it starts with "y=" or "x="
                (slope_intercept_eq.find("y") >= 0 and slope_intercept_eq.find("y") < slope_intercept_eq.find("=") and (
                        slope_intercept_eq.find("y") != 0 or slope_intercept_eq.find("=") != 1)) or
                (slope_intercept_eq.find("x") >= 0 and slope_intercept_eq.find("x") < slope_intercept_eq.find("=") and (
                        slope_intercept_eq.find("x") != 0 or slope_intercept_eq.find("=") != 1))
            ):
            raise ValueError("Line: equation inputted %r must be in valid y=mx+b form." % slope_intercept_eq)
        self.equation = slope_intercept_eq

    def get_slope(self):
        '''
        find slope given self.equation
        :return: float representing slope
        '''

        # parse equation to find slope
        equals_index = self.equation.find("=")
        x_index = self.equation.find("x")

        if x_index < 0:
            # if 'x' is not found in the slope-intercept form, then there is no slope, i.e. y=-2
            slope = 0.0
        elif (x_index < equals_index):
            # 'x' is before '=', so this is a vertical line, i.e. x=4
            slope = "DNE"
        else:
            # standard y-intercept form, i.e. y=8x-7
            m = self.equation[equals_index + 1:x_index]

            try:
                slope = float(m)
            except ValueError as e:
                # reraise it with custom message
                error_msg_output = "get_slope: slope cannot be found for %s!" % self.equation
                print(error_msg_output)
                e.args += (error_msg_output,)
                raise

        return slope

    def get_y_intercept(self):
        '''
        find y-intercept given self.equation
        :return: float representing y_intercept
        '''

        # get y intercept from slope-intercept form, must start from slope to avoid missing + or - signs

        # parse the equation
        x_index = self.equation.find("x")
        equals_index = self.equation.find("=")

        # it is a vertical line, i.e. x=4
        if (x_index < equals_index and x_index >= 0 and equals_index >= 0):
            b = "DNE"
        else:
            # if there isn't slope, then just get the y-intercept
            if (x_index < 0):
                x_index = equals_index

            # b is after the sign after the x, i.e. b=3 when y=5x+3
            y_intercept = self.equation[x_index + 1:]

            try:
                b = float(y_intercept)
            except ValueError as e:
                # reraise it with custom message
                error_msg_output = "get_y_intercept: y_intercept cannot be found for %s!" % self.equation
                print(error_msg_output)
                e.args += (error_msg_output,)
                raise

        return b

    def get_x_intercept(self):
        '''
        find x-intercept given self.equation
        :return: float representing x_intercept
        '''
        # parse the equation
        x_index = self.equation.find("x")
        equals_index = self.equation.find("=")

        x_inter = 0.0
        if x_index < 0:
            # if x is not found in the equation, then it must not be crossing the x-axis, i.e. y=5
            x_inter = "DNE"
        elif (self.get_slope() == 0):
            x_inter = "DNE"
        else:

            if (x_index < equals_index):
                # x_intercept is simply the line i.e. x=3
                x_intercept = self.equation[equals_index + 1:]
            else:
                # find x intercept by setting y to 0 i.e. 0 = 4x+6 and isolating x, i.e. x= -6/4
                x_intercept = (-self.get_y_intercept()) / self.get_slope()

            try:
                x_inter = float(x_intercept)
            except ValueError as e:
                # reraise it with custom message
                error_msg_output = "get_x_intercept: x_intercept cannot be found!" % self.equation
                print(error_msg_output)
                e.args += (error_msg_output,)
                raise

        return x_inter
