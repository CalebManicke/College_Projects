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
# Convenient helper function that will tell us how point c is oriented towards tangent line formed by (a, b)
# collinear, cw and ccw helper functions above produce runtime errors for certain random inputs
def findOrientation(a, b, c):
    # Compute slopes of line segments from points a to b and b to c respectively
    slope_a_to_b = (b[1]-a[1]) * (c[0]-b[0]) 
    slope_b_to_c = (c[1]-b[1]) * (b[0]-a[0])
    # If slope from a to b is equal to slope from b to c, it's collinear: greater --> triplet has clockwise orientation, lesser --> counterclockwise orientation
    if slope_a_to_b == slope_b_to_c:  return 0  
    elif slope_a_to_b > slope_b_to_c: return 1
    else: return -1


def findTangents(left_hull, right_hull):
    # Find the indexes of the rightmost point of the left hull and the leftmost point of the right hull: O(n)
    left_index, right_index = 0, 0
    for i in range(len(left_hull)):
        if left_hull[i] > left_hull[left_index]:
            left_index = i
    for i in range(len(right_hull)):
        if right_hull[i] < right_hull[right_index]:
            right_index = i

    # We will iterate through each point in left_hull and right_hull to find the upper tangent: O(n)
    while True:
        # If our current tangent line (left_hull[left_index], right_hull[right_index]) is NOT counterclockwise to our clockwise point on right_hull, we move right_index clockwise
        if findOrientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index + 1) % len(right_hull)]) < 0: # >
            right_index = (right_index + 1) % len(right_hull)
        # If our current tangent line is NOT clockwise to our counterclockwise point of left_hull, we move left_index counterclockwise
        elif findOrientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index + len(left_hull) - 1) % len(left_hull)]) > 0: # <=
            left_index = (left_index + len(left_hull)- 1) % len(left_hull)
        # If our point at left_index is counterclockwise to left_hull and right_index is clockwise to right_hull, we've found out point
        else:
            break 
    upper = (left_index, right_index)

    # Find the indexes of the leftmost point of the left hull and the rightmost point of the right hull: O(n)
    left_index, right_index = 0, 0
    for i in range(len(left_hull)):
        if left_hull[i] < left_hull[left_index]:
            left_index = i
    for i in range(len(right_hull)):
        if right_hull[i] > right_hull[right_index]:
            right_index = i

    # Iterate through left_hull and right_hull to find lower tangent: O(n)
    while True:
        # If our current tangent line (left_hull[left_index], right_hull[right_index]) is counterclockwise to our clockwise point on right_hull, we move right_index clockwise
        if findOrientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index + len(right_hull) - 1) % len(right_hull)]) > 0: #<
            right_index = (right_index + len(right_hull) - 1) % len(right_hull)
        # If our current tangent line is NOT clockwise to our counterclockwise point of left_hull, we move left_index counterclockwise
        elif findOrientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index + 1) % len(left_hull)]) < 0: # >=
            left_index = (left_index + 1) % len(left_hull)
        # If our point at left_index is clockwise to left_hull and right_index is counterclockwise to right_hull, we've found out point 
        else:
            break
    lower = (left_index, right_index)

    return upper, lower


def mergeHulls(left_hull, right_hull):
    # Sort points in left_hull and right_hull in counterclockwise order: O(n log (n)) -- Approximately = O(n)
    clockwiseSort(left_hull)
    clockwiseSort(right_hull)
    #left_hull.reverse()
    #right_hull.reverse()

    # Find the upper tangent and lower tangent of the hulls
    upper, lower = findTangents(left_hull, right_hull)

    # Merge the hulls using the upper and lower tangents
    merged_hull = []

    # Merge points in left_hull to the left of upper and lower tangents 
    i = upper[0]
    while i != lower[0]:
        merged_hull.append(left_hull[i])
        i = (i+ 1) % len(left_hull)
    merged_hull.append(left_hull[lower[0]])

    # Merge points in right_hull to the right of upper and lower tangents
    i = lower[1]
    while i != upper[1]:
        merged_hull.append(right_hull[i])
        i = (i+ 1) % len(right_hull)
    merged_hull.append(right_hull[upper[1]])
    print(merged_hull)

    return merged_hull

def computeHull(points, initial = True):
    # If we have three points or less, we have a triangle, line or single point which is its own convex hull
    if len(points) <= 3: return points  

    # Sort the points by x-coordinate
    if initial:
        points = sorted(points, key=lambda x: (x[0], x[1])) # (x[0], x[1]))
        initial = False

    # Recursively find the convex hulls of the left and right point sets
    mid = len(points) // 2
    left_hull = computeHull(points[:mid], initial)
    right_hull = computeHull(points[mid:], initial)

    # Merge the convex hulls of the left and right point sets
    convex_hull = mergeHulls(left_hull, right_hull)

    return convex_hull
