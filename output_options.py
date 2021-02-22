import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from itertools import cycle


def visualize_symmetry(lines_of_symmetry_dict, slopes, y_intercepts, x_intercepts, output_dir=None):
    '''
    visualize points, line(s) of symmetry, and points reflected over line(s) of symmetry

    :param lines_of_symmetry_dict: dictionary outputted by symmetry(), in {((x1,y1), (y1,y2)): line_of_symmetry} format.
    :param slopes: slopes for each line of symmetry in the values of lines_points
    :param y_intercepts: y-intercept for each line of symmetry in the values of lines_points
    :param x_intercepts: x-intercept for each line of symmetry in the values of lines_points
    :param output_dir: directory to output the resulting figure, if any
    :return: None
    '''
    # get min and max of the reflected points and points to set the range of the map
    x_min = min([float(key_point[0])
                 for key_points in lines_of_symmetry_dict.keys() for key_point in key_points])
    x_max = max([float(key_point[0]) for key_points in lines_of_symmetry_dict.keys() for key_point in key_points])

    y_min = min([float(key_point[1]) for key_points in lines_of_symmetry_dict.keys() for key_point in key_points])
    y_max = max([float(key_point[1]) for key_points in lines_of_symmetry_dict.keys() for key_point in key_points])

    range_min = min(x_min, y_min)
    range_max = max(x_max, y_max)

    # indexing for lines, keeping track of which line currently being looked at
    line_i = 0

    # aggregate dataframe to later plot all points and lines
    all_points = []
    all_x_lines = []
    all_y_lines = []
    all_lines_of_sym = []

    ########################
    ### individual plots ###
    ########################

    for points, line_of_symmetry in lines_of_symmetry_dict.items():
        point1 = points[0]
        point2 = points[1]
        m = slopes[line_i]
        b = y_intercepts[line_i]
        if (m != "DNE" and b != "DNE"):
            # extend line pass the range
            line_x_vals = np.linspace(range_min - 100, range_max + 100, 100)
            line_y_vals = (m * line_x_vals) + b
        else:
            # vertical line
            line_x_vals = [x_intercepts[line_i]] * 100
            line_y_vals = np.linspace(range_min - 100, range_max + 100, 100)
        # x values and y value currently being looked at
        point_x_vals = float(point1[0]), float(point2[0])
        point_y_vals = float(point1[1]), float(point2[1])

        # adding to aggregate dataframes to later plot all points and lines
        if point1 not in all_points:
            all_points.append(point1)
        if point2 not in all_points:
            all_points.append(point2)
        all_x_lines.append(line_x_vals)
        all_y_lines.append(line_y_vals)
        all_lines_of_sym.append(line_of_symmetry)

        line_i += 1

        # plotting
        # initializing figure
        points_str = '_'.join(str(v) for v in points[0]) + '__' + '_'.join(str(v) for v in points[1])
        file_name = "symmetry_%s.png" % (points_str)

        fig = plt.figure(file_name)
        ax = plt.gca()

        # set limits for display
        plt.xlim([range_min - 20, range_max + 20])
        plt.ylim([range_min - 20, range_max + 20])

        # set increments so x and y are on the same scale, integers so it's cleaner
        plt.xticks(np.arange(range_min, range_max, int((range_max - range_min) / 10)))
        plt.yticks(np.arange(range_min, range_max, int((range_max - range_min) / 10)))

        # plot line and points
        plt.plot(line_x_vals, line_y_vals, '--', color="green", label=line_of_symmetry)
        plt.scatter(point_x_vals, point_y_vals, c="orange", marker='o', label="Given Points")

        # annotate the points
        for point_xy in zip(point_x_vals, point_y_vals):
            ax.annotate('(%s, %s)' % point_xy, xy=point_xy, textcoords='data')

        # custom plot functions
        plt.title("line of symmetry for %r" % (points,))
        plt.grid()
        plt.legend()

        # save figure
        if output_dir:
            plt.savefig(os.path.join(output_dir, file_name))

        plt.show()
        plt.close()

    ######################
    ### aggregate plot ###
    ######################

    fig = plt.figure("aggregate symmetry for all given points")
    ax = plt.gca()

    # set limits for display
    plt.xlim([range_min - 20, range_max + 20])
    plt.ylim([range_min - 20, range_max + 20])

    # set increments so x and y are on the same scale, integers so it's cleaner
    plt.xticks(np.arange(range_min, range_max, int((range_max - range_min) / 10)))
    plt.yticks(np.arange(range_min, range_max, int((range_max - range_min) / 10)))

    # get all the x and ys in separate structure
    all_x_points = []
    all_y_points = []
    for point in all_points:
        all_x_points.append(float(point[0]))
        all_y_points.append(float(point[1]))

    # setting colors
    color_range = np.arange(len(all_points))
    # changing colors: https://stackoverflow.com/questions/37890412/increment-matplotlib-color-cycle
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = cycle(prop_cycle.by_key()['color'])

    # plot all the lines and all the points
    for line in range(len(all_x_lines)):
        plt.plot(all_x_lines[line], all_y_lines[line], '--', color=next(colors), label=all_lines_of_sym[line])
    plt.scatter(all_x_points, all_y_points, c=color_range, marker='o', label="Given Points")

    # annotate the points
    for point_xy in zip(all_x_points, all_y_points):
        ax.annotate('(%s, %s)' % point_xy, xy=point_xy, textcoords='data')

    # custom plot functions
    plt.title("aggregate line of symmetry for all points")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left', prop={'size': 6})
    plt.tight_layout(rect=[0, 0, 0.75, 1])
    # save figure
    if output_dir:
        plt.savefig(os.path.join(output_dir, file_name), bbox_inches="tight")

    plt.show()
    plt.close()

    return


def visualize_reflection(points, all_reflected_points, slopes, y_intercepts, x_intercepts, output_dir=None):
    '''
    visualize  reflection from given points to newly reflected points and lines of symmetry

    :param points: given points, in tuple or list
    :param all_reflected_points: a dictionary resulted from symmetry(), i.e. {"y=2x+2", [(3,3),(-2,-8)]}
    :param slopes: slope for each line of symmetry in the keys of all_reflected_points
    :param y_intercepts: y-intercept for each line of symmetry in the keys of all_reflected_points
    :param x_intercepts: x_intercept for each line of symmetry in the keys of all_reflected_points
    :param output_dir: save PNG of the plot if given output directory path
    :return: None
    '''

    # get min and max of the reflected points and points to set the range of the map
    x_min = min([values[0] for list_of_values in all_reflected_points.values() for values in list_of_values])
    x_max = max([values[0] for list_of_values in all_reflected_points.values() for values in list_of_values])

    y_min = min([values[1] for list_of_values in all_reflected_points.values() for values in list_of_values])
    y_max = max([values[1] for list_of_values in all_reflected_points.values() for values in list_of_values])

    range_min = min(x_min, y_min)
    range_max = max(x_max, y_max)

    line_i = 0
    # make a plot for each line of symmetry
    for key, vals in all_reflected_points.items():

        # parse line and points in proper format
        # line of symmetry
        m = slopes[line_i]
        b = y_intercepts[line_i]
        if (m != "DNE" and b != "DNE"):
            # extend line pass the range
            line_x_vals = np.linspace(range_min - 100, range_max + 100, 100)
            line_y_vals = (m * line_x_vals) + b

        else:
            # vertical line
            line_x_vals = [x_intercepts[line_i]] * 100
            line_y_vals = np.linspace(range_min - 100, range_max + 100, 100)

        # given points
        point_x_vals = [p[0] for p in points]
        point_y_vals = [p[1] for p in points]

        # reflected points
        reflected_x_vals = []
        reflected_y_vals = []
        for val in vals:
            x = val[0]
            y = val[1]
            reflected_x_vals.append(x)
            reflected_y_vals.append(y)

        # increment so next graph will get the correct slope and intercepts
        line_i += 1

        # initializing figure
        fig = plt.figure("reflection_%s.png" % key)
        ax = plt.gca()

        # set limits for display
        plt.xlim([range_min - 20, range_max + 20])
        plt.ylim([range_min - 20, range_max + 20])

        # set increments so x and y are on the same scale
        plt.xticks(np.arange(range_min, range_max, (range_max - range_min) / 10))
        plt.yticks(np.arange(range_min, range_max, (range_max - range_min) / 10))

        color_range = np.arange(len(point_x_vals))

        # plot
        line_sym_plot = ax.plot(line_x_vals, line_y_vals, '--', color="green", label=key)
        plt.scatter(point_x_vals, point_y_vals, c=color_range, marker='o')
        reflected_points = plt.scatter(reflected_x_vals, reflected_y_vals, c=color_range, marker='o')
        # differentiate the reflected points
        reflected_points.set_facecolor('none')

        # annotate the points
        for point_xy in zip(point_x_vals, point_y_vals):
            ax.annotate('(%s, %s)' % point_xy, xy=point_xy, textcoords='data')
        for reflected_xy in zip(reflected_x_vals, reflected_y_vals):
            ax.annotate('(%s, %s)' % reflected_xy, xy=reflected_xy, textcoords='data')
        # custom plot functions
        plt.title("reflected points for %r" % key)
        plt.grid()

        # custom legends
        line1 = plt.Line2D(range(1), range(1), color="black", marker='o', linestyle='None', label='Given Points')
        line2 = plt.Line2D(range(1), range(1), color="black", marker='o', markerfacecolor="none", linestyle='None',
                           label='Reflected Points')
        ax.legend(handles=[line_sym_plot[0], line1, line2])

        # save figure
        if output_dir:
            plt.savefig(os.path.join(output_dir, "reflection_%s.png" % key))

        plt.show()
        plt.close()


def write_symmetry_to_csv(lines_of_symmetry_dict, output_directory):
    '''
    write out points, and their line(s) of symmetry into a CSV

    :param lines_of_symmetry_dict: dictionary outputted by symmetry(), in {((x1,y1), (y1,y2)): line_of_symmetry} format.
    :param output_directory: directory path to output CSV
    :return: path in which the CSV is outputted
    '''

    # create a new directory for results
    new_dir = os.path.join(output_directory, "symmetry")
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    # write out dictionary into CSV
    with open(os.path.join(new_dir, 'symmetry.csv'), 'w') as f:
        # create writer and define column names
        writer = csv.DictWriter(f, fieldnames=["point_1", "point_2", "line_of_symmetry"])
        writer.writeheader()

        # write out line by line
        for key, val in lines_of_symmetry_dict.items():
            writer.writerow({"point_1": key[0], "point_2": key[1], "line_of_symmetry": val})

    return new_dir


def write_reflection_to_csv(points, all_reflected_points, output_directory):
    '''
    write out points, line of symmetry, and the resulting reflected points into a CSV

    :param points: given points, in tuple or list
    :param all_reflected_points: a dictionary resulted from symmetry(), i.e. {"y=2x+2", [(3,3),(-2,-8)]}
    :param output_directory: directory path to output CSV
    :return: path in which the CSV is outputted
    '''

    # create a new directory for results
    new_dir = os.path.join(output_directory, "reflection")
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    # write out dictionary into CSV
    with open(os.path.join(new_dir, 'reflection.csv'), 'w') as f:
        # create writer and define column names
        writer = csv.DictWriter(f, fieldnames=["line_of_symmetry", "given_points", "reflected_points"])
        writer.writeheader()

        # write out line by line
        for key in all_reflected_points:
            i = 0
            for reflected_point in all_reflected_points[key]:
                writer.writerow(
                    {"line_of_symmetry": key, "given_points": points[i], "reflected_points": reflected_point})
                i += 1

    return new_dir
