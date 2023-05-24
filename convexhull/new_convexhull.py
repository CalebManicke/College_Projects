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
# Find orientation of directed triangle formed by (a, b, c) by comparing slopes: O(1)
# Note: collinear, cw and ccw helper functions above produce runtime errors for certain random inputs
def findOrientation(a, b, c):
    # Compute orientation terms derived from slopes of tangents from points a to b and b to c respectively
    a_to_b_orientation = (b[1] - a[1]) * (c[0] - b[0]) 
    b_to_c_orientation = (b[0] - a[0]) * (c[1] - b[1])
    # If slope from a to b is equal to slope from b to c, it's collinear: greater --> triplet has clockwise orientation, lesser --> counterclockwise orientation
    if ((a_to_b_orientation - b_to_c_orientation) == 0):  return 0  
    elif (a_to_b_orientation > b_to_c_orientation): return 1
    else: return -1


def findTangents(left_hull, right_hull):
    # Find the indexes of the rightmost point of the left hull and the leftmost point of the right hull: O(n)
    left_index, right_index = 0, 0
    for i in range(len(left_hull)):
        if left_hull[i][0] >= left_hull[left_index][0]:
            left_index = i
    for i in range(len(right_hull)):
        if right_hull[i][0] <= right_hull[right_index][0]:
            right_index = i

    # Iterate through each point in left_hull and right_hull to find the upper tangent: O(n)
    while True:
        # If triangle (p_i, q_i, q_{i+1}) is oriented clockwise, the tangent from p_i to q_{i+1} will be above tangent connected to q_i: move right_index clockwise
        if findOrientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index + 1) % len(right_hull)]) > 0:
            right_index = (right_index + 1) % len(right_hull) 
        # If triangle (q_i, p_i, p_{i-1}) is oriented counterclockwise, the tangent q_i to p_{i-1} is above tangent q_i to p_i: move left_index counterclockwise
        elif findOrientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index + len(left_hull) - 1) % len(left_hull)]) < 0:
            left_index = (left_index + len(left_hull) - 1) % len(left_hull)
        # Once we found maximally clockwise point for left_hull for forming a tangent with any point in right_hull above all points in left_hull, and maximal counterclockwise point in right_hull for same reason, break from loop
        else:
            break 
    upper = (left_index, right_index)

    # Find the indexes of the leftmost point of the left hull and the rightmost point of the right hull: O(n)
    left_index, right_index = 0, 0
    for i in range(len(left_hull)):
        if left_hull[i][0] <= left_hull[left_index][0]:
            left_index = i
    for i in range(len(right_hull)):
        if right_hull[i][0] >= right_hull[right_index][0]:
            right_index = i

    # Iterate through left_hull and right_hull to find lower tangent: O(n)
    while True:
        # If triangle (p_i, q_i, q_{i+1}) is oriented counterclockwise, the tangent formed from p_i to q_{i+1} is below tangent from p_i q_i: move right_index clockwise
        if findOrientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index + 1) % len(right_hull)]) < 0: 
            right_index = (right_index + 1) % len(right_hull)
        # If triangle (q_i, p_i, p_{i-1}) is oriented clockwise, the tangent q_i to p_{i-1} is below the tangent q_i to p_i: move left_index counterclockwise
        elif findOrientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index + len(left_hull) - 1) % len(left_hull)]) > 0: 
            left_index = (left_index + len(left_hull) - 1) % len(left_hull) 
        # We found p_i whose tangent with q_i is below all other points in left_hull and q_i whose tangent with p_i is below all other points in right_hull: break from loop
        else:
            break
    lower = (left_index, right_index)

    return upper, lower


def mergeHulls(left_hull, right_hull):
    # Sort points in left_hull and right_hull in counterclockwise order: O(n log (n)) 
    clockwiseSort(left_hull)
    clockwiseSort(right_hull)

    # Find the upper tangent and lower tangent of the hulls
    upper, lower = findTangents(left_hull, right_hull)

    # Merge the hulls using the upper and lower tangents
    merged_hull = []

    # Add points in left_hull to merged_hull, going clockwise from upper to lower tangent
    i = upper[0]
    while i != lower[0]:
        merged_hull.append(left_hull[i])
        i = (i + len(left_hull) - 1) % len(left_hull)
    merged_hull.append(left_hull[lower[0]])

    # Add points in right_hull to merged_hull, going clockwise from lower to upper tangent
    j = lower[1]
    while j != upper[1]:
        merged_hull.append(right_hull[j])
        j = (j + len(right_hull) - 1) % len(right_hull)
    merged_hull.append(right_hull[upper[1]])

    return merged_hull


def computeHull(points, initial = True):
    # If we have three points or less, we have a triangle, line or single point which is its own convex hull
    if len(points) <= 3: return points  

    # Sort the points by x-coordinate before making a recursive call, set initial = False so we don't sort by x-coordinates again
    if initial == True:
        points = sorted(points, key=lambda x: (x[0], x[1])) 
        initial = False

    # Recursively find the convex hulls of the left and right point sets
    mid = len(points) // 2
    left_hull = computeHull(points[:mid], initial)
    right_hull = computeHull(points[mid:], initial)

    # Merge left and right convex hulls
    convex_hull = mergeHulls(left_hull, right_hull)

    return convex_hull

# At each level, we make two recursive calls by passing in half of our points.
# Although finding the tangent lines is linear (only have to iterate through left_hull and right_hull), because we have to sort our hulls clockwise, our merge and combine steps are O(n log(n)).
# This gives us a Recurrence Relation of T(n) = { O(1) when n <= 3 , 2T(n/2) + O(n log(n)) otherwise
# We cannot solve this using Master's Theorem! Recurrence analysis will give us T(n) = O(n log^2 (n)).
# Our running time when compared to Merge Sort reflects this: although computeHull doesn't run substantially faster, with larger lists our difference begins to widen and even double. 