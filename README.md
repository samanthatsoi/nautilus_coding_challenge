## Nautilus Coding Challenge <br />
by Samantha Tsoi <br />
Date started: 2/22/2021 <br/>
<br />


#### Summary: <br />
1. Find line(s) of symmetry given a set of points on an infinite plane
2. Find reflected point(s) given point(s) and line(s) of symmetry, i.e. "x-axis", "y-axis", "y=-34x-29.4"

Results are outputted in ../symmetry/ or ../reflection/, respectively, with the option to visualize the solution and write out the CSVs containing the resulting point(s) and/or line(s).
<br />


<br />

#### Files: <br />
- get_symmetry_line.py : Python code
  + holds get_symmetry_line(), where it calculates line(s) of symmetry given list of point(s), for each unique combination of given set of points
- get_reflection_point.py : Python code
  + holds get_reflection_point(), where it calculates point(s) reflected given line(s) of symmetry and given point(s), for each unique combination of given points and lines
- computation.py : Python code
  + holds all the methods required to compute get_symmetry_line() and get_reflection_point()
- Line.py : Python code
  + Line class/object is used to represent a line in a 2D plane given an equation in slope-intercept form, x=x1, or y=y1, i.e. y=3x-231.4, x=2, y=-34421.6
- output_options.py : Python code
  + holds the methods that customizes ways to output the solution, including visualizing using matplotlib library and writing out to CSV
- main.py: Python code
  + a sample script that runs get_symmetry_line() and get_reflection_point() given sample inputs.

<br />
<br />
