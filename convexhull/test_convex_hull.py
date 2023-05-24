import unittest, random
import new_convexhull as convexhull
import matplotlib.pyplot as plt
import time

# We use mergesort to benchmark running time (How does computeHull's running time compare to a logarithmic algorithm?)
def mergesort(L):
    if len(L) <= 1: return L 

    median = len(L) // 2
    left = L[:median]  
    right = L[median:] 

    left = mergesort(left)
    right = mergesort(right)

    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            L[i+j] = left[i]
            i += 1 
        else:
            L[i + j] = right[j]
            j += 1

    L[i+j:] = left[i:] + right[j:] 
    return L    


class TestConvexHull(unittest.TestCase):
    def test_convex_hull_base_cases(self):
        # Base Cases: These sets of points describe a point, line, and triangle respectively
        points_1 = [(2, 3)]
        points_2 = [(1, 3), (2, 3)]
        points_3 = [(1, 3), (4, 6), (3, 7)]

        # A point, line, and triangle are their own convex hulls: therefore, our function should just return them as they are
        self.assertEqual(convexhull.computeHull(points_1), points_1)
        self.assertEqual(convexhull.computeHull(points_2), points_2)
        self.assertEqual(convexhull.computeHull(points_3), points_3)


    def test_tangent_merge_set_triangles(self):
        # We have two defined sets of triangles, we will call findTangets and mergeHulls to see how our tangents form one level above our base case
        points_x = [30, 40, 50, 60, 70, 80]
        points_y = [70, 20, 30, 50, 40, 70]
        triangle1, triangle2 = [(30, 70), (40, 20), (50, 30)], [(60, 50), (70, 40), (80, 70)]

        convex_hull = convexhull.mergeHulls(triangle1, triangle2)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        # Points in our first triangle are marked by a blue circle, points in our second triangle are marked by an orange triangle
        plt.plot(points_x[:len(points_x)//2] + [points_x[0]], points_y[:len(points_x)//2] + [points_y[0]], '--o')
        plt.plot(points_x[len(points_x)//2:] + [points_x[3]], points_y[len(points_x)//2:] + [points_y[3]], '--^')
        plot_convex_x = [convex_hull[i][0] for i in range(len(convex_hull))]
        plot_convex_x.append(convex_hull[0][0])
        plot_convex_y = [convex_hull[i][1] for i in range(len(convex_hull))]
        plot_convex_y.append(convex_hull[0][1])
        # Points in our convex hull are connected by a blue dotted line
        plt.plot(plot_convex_x, plot_convex_y, '--bo')
        plt.title('Merge Defined Triangles')
        plt.show()


    def test_convex_hull_three_random_triangles(self):
        # Create two random triangles, test computeHull
        # 6 points means after 1 merge step, we will find the convex hull for two triangles (one recursive level)
        points = [(random.randrange(0, 100, 1), random.randrange(0, 100, 1)) for i in range(6)]
        points_x = [points[i][0] for i in range(len(points))]
        points_y = [points[i][1] for i in range(len(points))]

        convex_hull = convexhull.computeHull(points)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.plot(points_x, points_y, 'o')
        plot_convex_x = [convex_hull[i][0] for i in range(len(convex_hull))]
        plot_convex_x.append(convex_hull[0][0])
        plot_convex_y = [convex_hull[i][1] for i in range(len(convex_hull))]
        plot_convex_y.append(convex_hull[0][1])
        plt.plot(plot_convex_x, plot_convex_y, '--bo')
        plt.title('Find Convex Hull for Random Triangles')
        plt.show()


    def test_tangent_merge_set_polygons(self):
        # We define two polygons, we call mergeHull to see how combining more complicated shapes works
        points_x = [11, 23, 34, 54, 55, 76, 87, 89, 90, 99]
        points_y = [30, 42, 11, 54, 37, 87, 99, 31, 34, 45]
        polygon1, polygon2 = [], []
        for i in range(len(points_x)//2):
            polygon1.append((points_x[i], points_y[i]))
            polygon2.append((points_x[i+len(points_x)//2], points_y[i+len(points_x)//2]))

        convex_hull = convexhull.mergeHulls(polygon1, polygon2)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        # Points in polygon1 and polygon2 represented by blue circles and orange triangles respectively
        plt.plot(points_x[:len(points_x)//2] + [points_x[5]], points_y[:len(points_x)//2] + [points_y[5]], '--o')
        plt.plot(points_x[len(points_x)//2:] + [points_x[0]], points_y[len(points_x)//2:] + [points_y[0]], '--^')
        plot_convex_x = [convex_hull[i][0] for i in range(len(convex_hull))]
        plot_convex_x.append(convex_hull[0][0])
        plot_convex_y = [convex_hull[i][1] for i in range(len(convex_hull))]
        plot_convex_y.append(convex_hull[0][1])
        plt.plot(plot_convex_x, plot_convex_y, '--bo')
        plt.title('Merge 10-sided defined polynomials')
        plt.show()


    def test_convex_hull_random_n_points(self):
        n = 1000
        # We generate n random points, print our result to make sure our Convex Hull is clockwise
        points = [(random.randrange(0, n, 1), random.randrange(0, n, 1)) for i in range(n)]
        points_x = [points[i][0] for i in range(len(points))]
        points_y = [points[i][1] for i in range(len(points))]

        convex_hull = convexhull.computeHull(points)
        print("100 Random Points Convex Hull: ", convex_hull)
        
        plt.xlim(0, n)
        plt.ylim(0, n)
        plt.plot(points_x, points_y, 'o')
        plot_convex_x = [convex_hull[i][0] for i in range(len(convex_hull))]
        plot_convex_x.append(convex_hull[0][0])
        plot_convex_y = [convex_hull[i][1] for i in range(len(convex_hull))]
        plot_convex_y.append(convex_hull[0][1])
        plt.plot(plot_convex_x, plot_convex_y, '--bo')
        plt.title('Convex Hull for n Random Points')
        plt.show()


    def test_debugging_hard_example(self):
        # This is a randomly generated example of 100 points that our convexhull function struggled with...
        points = [(76, 63), (81, 1), (79, 38), (55, 95), (1, 51), (59, 40), (54, 3), (84, 38), (82, 3), (50, 75), (66, 70), (79, 50), (55, 95), (85, 69), (45, 34), (39, 28), (39, 28), (34, 41), (59, 46), (32, 70), (40, 45), (85, 81), (39, 91), (96, 84), (53, 83), (38, 27), (44, 49), (22, 76), (83, 6), (74, 32), (13, 37), (74, 23), (67, 53), (14, 96), (22, 69), (52, 19), (33, 21), (41, 43), (62, 51), (20, 0), (79, 2), (37, 78), (84, 16), (56, 73), (25, 89), (97, 80), (48, 51), (36, 69), (8, 75), (81, 60), (98, 55), (75, 14), (9, 92), (45, 87), (47, 5), (24, 87), (72, 91), (39, 8), (26, 2), (29, 73), (25, 14), (37, 78), (83, 1), (58, 36), (19, 54), (94, 81), (39, 20), (37, 15), (43, 15), (83, 70), (49, 97), (13, 90), (33, 51), (1, 83), (10, 25), (59, 76), (9, 54), (25, 29), (21, 65), (74, 90), (67, 75), (54, 81), (70, 42), (88, 91), (95, 24), (4, 4), (69, 87), (44, 70), (56, 18), (61, 55), (95, 29), (62, 34), (89, 9), (84, 0), (41, 22), (36, 84), (80, 53), (84, 0), (20, 65), (10, 1), (20, 0), (10, 1), (4, 4), (1, 51), (1, 83), (9, 92), (14, 96), (96, 84), (97, 80), (98, 55), (95, 24), (89, 9), (84, 0), (84, 0)]
        points_x = [points[i][0] for i in range(len(points))]
        points_y = [points[i][1] for i in range(len(points))]

        convex_hull = convexhull.computeHull(points)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.plot(points_x, points_y, 'o')
        plot_convex_x = [convex_hull[i][0] for i in range(len(convex_hull))]
        plot_convex_x.append(convex_hull[0][0])
        plot_convex_y = [convex_hull[i][1] for i in range(len(convex_hull))]
        plot_convex_y.append(convex_hull[0][1])
        plt.plot(plot_convex_x, plot_convex_y, '--bo')
        plt.title('Convex Hull for Hard Example')
        plt.show()


    def test_running_time(self):
        # Create a list of list_size[i] random elements 
        list_sizes = [10, 100, 200, 500, 1000, 1500, 2000]
        rand_points = []
        for size in list_sizes:
            rand_points.append([(random.randrange(0, 100, 1), random.randrange(0, 100, 1)) for j in range(size)])
        computeHull_times = []
        mergeSort_times = []

        # For each list size, record computeHull's running time as well as MergeSort's
        for i in range(len(list_sizes)):
            computeHull_start_time = time.time()
            convexhull.computeHull(rand_points[i])
            computeHull_end_time = time.time()
            computeHull_times.append(computeHull_end_time - computeHull_start_time)

            x_points = [point[0] for point in rand_points[i]]
            mergesort_start_time = time.time()
            mergesort(x_points)
            mergesort_end_time = time.time()
            mergeSort_times.append(mergesort_end_time - mergesort_start_time)

        # Create table of running times for a sorted and unsorted list of each size
        headers = ("________________________________", "______________Compute Hull_____________", "______________Merge Sort______________")
        print(headers[0], "|", headers[1], "|", headers[2])
        for i in range(len(list_sizes)):  print("List Size: ", list_sizes[i], " " * (len(headers[0]) - len("List Size: " + str(list_sizes[i])) - 2), "| ", computeHull_times[i], " " * (len(headers[1]) - len(str(computeHull_times[i])) - 2), "| ", mergeSort_times[i])

if __name__ == '__main__':
    unittest.main()
    