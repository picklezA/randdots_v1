# version: 0.0.2
# author: picklez

import cv2
import numpy
import random
import math

def draw_black(array):
    for col in range(len(array)):
        for row in range(len(array[-1])):
            array[col][row][0] = 0
            array[col][row][1] = 0
            array[col][row][2] = 0
    return array

def draw_white(array):
    for col in range(len(array)):
        for row in range(len(array[-1])):
            array[col][row][0] = 255
            array[col][row][1] = 255
            array[col][row][2] = 255
    return array

def create_random_dots(array):
    amt_of_dots = 150
    dot_array = []
    deviation = 1
    size_y = list(range(0, len(array)))
    size_x = list(range(0, len(array[-1])))
    while amt_of_dots != 0:
        new_dot = []
        new_x = random.randrange(0+deviation, len(size_x)-deviation)
        new_y = random.randrange(0+deviation, len(size_y)-deviation)
        sub_coords = []
        sub_coords.append(size_y[new_y])
        sub_coords.append(size_x[new_x])
        
        # time to remove random generated stuff
        for x in range((deviation*2)+1):
            size_y.pop(new_y-deviation)
            size_x.pop(new_x-deviation)
        
        dot_array.append(sub_coords)
        
        amt_of_dots -= 1
    return sorted(dot_array)

def find_distance(dot1, dot2):
    d_x = abs(dot2[0]) - abs(dot1[0])
    d_y = abs(dot2[1]) - abs(dot1[1])
    distance = math.sqrt((d_x*d_x)+(d_y*d_y))
    return round(distance, 2)
    
def nearest(dot_array): # returns the 5 nearest dot to a given dot
    nearest = {}
    for dot in dot_array:
        sub_nearest = {}
        distance_array = []
        sub_dot_array = dot_array
        sub_dot_array.remove(dot)
        for dot2 in sub_dot_array:
            distance = find_distance(dot, dot2)
            sub_nearest[str(distance)] = dot2
            distance_array.append(distance)
        distance_array=sorted(distance_array)
        to_add = []
        for i in range(10):
            to_add.append(sub_nearest[str(distance_array[i])])
        nearest[str(dot)] = to_add
    return nearest

def line(point1, point2):
    point1 = point1.replace("[","").replace("]","").split(", ")
    for i in range(len(point1)):
        point1[i] = int(point1[i])
    all_points_between = []
    # y = mx + b
    dtop = point2[0] - point1[0]
    dbot = point2[1] - point1[1]
    m = dtop / dbot
    b = point1[0] - (m * point1[1])
    if point1[1] < point2[1]:
        for i in range(point1[1],point2[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    if point1[1] > point2[1]:
        for i in range(point2[1],point1[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    return all_points_between

def draw_lines(new_image, nearest):
    for key in nearest:
        for point in nearest[key]:
            line_array = line(key, point)
            r_or_b = random.randrange(0,2)
            for point2 in line_array:
                if r_or_b == 0:
                    new_image[point2[0]][point2[1]][0] = 255
                    new_image[point2[0]][point2[1]][1] = 0
                    new_image[point2[0]][point2[1]][2] = 0
                if r_or_b == 1:
                    new_image[point2[0]][point2[1]][0] = 0
                    new_image[point2[0]][point2[1]][1] = 0
                    new_image[point2[0]][point2[1]][2] = 255
    return new_image

def apply_dots(new_image, dot_array):
    for dot in dot_array:
        # center of dot
        new_image[dot[0]][dot[1]][0] = 255
        new_image[dot[0]][dot[1]][1] = 255
        new_image[dot[0]][dot[1]][2] = 255
        
        # outside edge of dot
        new_image[dot[0]+1][dot[1]][0] = 0
        new_image[dot[0]+1][dot[1]][1] = 255
        new_image[dot[0]+1][dot[1]][2] = 0
        new_image[dot[0]][dot[1]+1][0] = 0
        new_image[dot[0]][dot[1]+1][1] = 255
        new_image[dot[0]][dot[1]+1][2] = 0
        new_image[dot[0]-1][dot[1]][0] = 0
        new_image[dot[0]-1][dot[1]][1] = 255
        new_image[dot[0]-1][dot[1]][2] = 0
        new_image[dot[0]][dot[1]-1][0] = 0
        new_image[dot[0]][dot[1]-1][1] = 255
        new_image[dot[0]][dot[1]-1][2] = 0
        
        
    return new_image

# define the array we would like to manipulate
new_image = numpy.empty((720,1080,3))

new_image = draw_black(new_image)
dot_array = create_random_dots(new_image)
dot_image = apply_dots(new_image, dot_array)
nearest_dots_map = nearest(dot_array)
dot_image = draw_lines(dot_image, nearest_dots_map)

cv2.imshow("new_image", dot_image)
cv2.waitKey()