import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	#angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = lambda p: ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi)))

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
# change is either -1 or 1
def circle_move(pointer, points, change):
	if pointer + change == -1:
		return len(points) - 1
	if pointer + change == len(points):
		return 0
	return pointer + change

# Compute tangent slope and intercept given two points
def compute_tangent(p1, p2):
	if p1[0] < p2[0]:
		m = (p2[1] - p1[1])/(p2[0] - p1[0])
	if p2[0] < p1[0]:
		m = (p1[1] - p2[1])/(p1[0] - p2[0])
	else:
		m = 0
	b = p1[1] - m * p1[0]
	return m, b

# Find lower and upper tangent in O(n) by comparing points in left and right
def find_tangent(left, right, which_tangent):
	# Save lambda function for finding upper and lower tangent
	neighbor_relation = 0
	if which_tangent == 'lower':
		neighbor_relation = lambda x, y: x > y 
	if which_tangent == 'upper':
		neighbor_relation = lambda x, y: x < y 

	# Sort each set of points so we have a clockwise rotation
	clockwiseSort(left)
	clockwiseSort(right)

	# Keep track of pointers for each point set
	left_point = len(left) - 1
	right_point = 0

	# Compute median point for tangent line between points at left_point and right_point
	lower_tangent_found = False
	while lower_tangent_found == False:
		m, b = compute_tangent(left[left_point], right[right_point])

		# Check neighbors of left_point
		left_point_left = circle_move(left_point, left, -1)
		left_point_right = circle_move(left_point, left, 1)
		# If both neighbors are above our tangent line, we've found a lower tangent for left_point
		if neighbor_relation(left[left_point_left][1],  m * left[left_point_left][0] + b) and neighbor_relation(left[left_point_right][1], m * left[left_point_right][0] + b):
			lower_tangent_found = True
		else: 
			left_point = left_point_left

		# Check neighbors of right_point
		right_point_left = circle_move(right_point, right, -1)
		right_point_right = circle_move(right_point, right, 1)
		# Check if both neighbors are above tangent line of left_point and right_point
		if neighbor_relation(right[right_point_left][1], m * right[right_point_left][0] + b) and neighbor_relation(right[right_point_right][1], m * right[right_point_right][0] + b):
			lower_tangent_found = True
		else: 
			right_point = right_point_right

	# Return tuple of pointers whose points have lower tangent between left and right point sets
	print((left_point, right_point))
	return (left_point, right_point)


def computeHull(points, initial = True):
	# If we only have three points, we have a triangle which is its own convex hull: return points
	if len(points) <= 3: return points

	# Sort based on x-coordinate for initial call, takes O(n log(n))
	if initial == True: points = sorted(points, key = lambda x: x[0], reverse = True)

	# Divide points into two halves, recurse until base case
	med = len(points) // 2
	left = computeHull(points[: med], initial = False)
	right = computeHull(points[med: ], initial = False)
	print("Left: ", points[: med])
	print("Right: ", points[med:])

	# Find lower and upper tangent tuples
	lower_T = find_tangent(left, right, 'lower')
	upper_T = find_tangent(left, right, 'upper')

	left_point = lower_T[0]
	right_point = upper_T[1]

	# Merge left and right points into one list
	merged_points = []

	while right[right_point] != right[lower_T[1]]:
		merged_points.append(right[right_point])
		right_point = circle_move(right_point, right, 1)

	while left[left_point] != left[upper_T[0]]:
		merged_points.append(left[left_point])
		left_point = circle_move(left_point, left, 1)

	return merged_points

def orientation(p, q, r):
    """Find the orientation of the triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise

def convex_hull(points):
    """Find the convex hull of a set of points."""
    n = len(points)
    if n < 3:
        return []  # not enough points for a hull

    # Find the point with the lowest y-coordinate, breaking ties by lowest x-coordinate
    min_idx = 0
    for i in range(1, n):
        if points[i][1] < points[min_idx][1]:
            min_idx = i
        elif points[i][1] == points[min_idx][1] and points[i][0] < points[min_idx][0]:
            min_idx = i

    # Swap the lowest point with the first point
    points[0], points[min_idx] = points[min_idx], points[0]

    # Sort the points by polar angle around the lowest point
    pivot = points[0]
    points = sorted(points[1:], key=lambda x: math.atan2(x[1] - pivot[1], x[0] - pivot[0]))

    # Initialize the stack with the first two points
    stack = [pivot, points[0]]

    # Iterate over the remaining points, adding them to the hull or popping from the stack
    for i in range(1, n-1):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()
        stack.append(points[i])

    # Add the last point to the hull
    stack.append(points[-1])

    return stack