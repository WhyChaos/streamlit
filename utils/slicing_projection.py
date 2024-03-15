
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from functools import lru_cache
import json


@lru_cache(maxsize=100) 
def slicing_projection(cut_x, cut_y, docs, background_image, ref_mask):
    docs = cv2.convertScaleAbs(np.array(json.loads(docs)))
    background_image = cv2.convertScaleAbs(np.array(json.loads(background_image)))
    ref_mask = cv2.convertScaleAbs(np.array(json.loads(ref_mask)))
    
    transformed_image=corresponding_projection_all(docs, background_image, ref_mask, height_num=cut_y, width_num=cut_x)
    return cv2.bitwise_and(background_image, transformed_image)

def find_docs_areas(docs, erea=[0,0], height_num=4, width_num=4):
    assert erea[0]>=0 and erea[0]<height_num
    assert erea[1]>=0 and erea[1]<width_num
    
    height, width, _ = docs.shape
    x = [erea[1]*width/width_num, (erea[1]+1)*width/width_num, (erea[1]+1)*width/width_num, erea[1]*width/width_num]
    y = [erea[0]*height/height_num, erea[0]*height/height_num, (erea[0]+1)*height/height_num, (erea[0]+1)*height/height_num]
    return docs[int(y[0]):int(y[2]+1), int(x[0]):int(x[1]+1)]

def find_corners(arr, scope=20, corner_dis=None):
    if corner_dis == None:
        corner_dis = min(*arr.shape)//10
    bool_array = arr == 255
    edges = cv2.Canny(arr, 100, 200)
    edges = edges == 255
    
    couters = []
    height, width = arr.shape
    cout = 0 
    for x in range(width):
        for y in range(height):
            if edges[y][x] == False:
                continue
            tmp = 0
            for i in range(-scope, scope+1, 1):
                xx = x + i
#                 for j in range(-math.floor(math.sqrt(scope**2-i**2)), math.floor(math.sqrt(scope**2-i**2))+1, 1):
                for j in [-math.floor(math.sqrt(scope**2-i**2)), math.floor(math.sqrt(scope**2-i**2))]:
                    yy = y + j
                    if xx < 0 or xx >= width or yy < 0 or yy >= height:
                        tmp+=1
                    elif bool_array[yy][xx] == False:
                        tmp+=1
            couters.append([x,y,tmp])   
            
    def compare_third_element(item):
        return item[2]
    def judge(corners, couter):
        for corner in corners:
            if (corner[0]-couter[0])**2 + (corner[1]-couter[1])**2 < corner_dis**2:
                return False
        return True
            
        
    couters = sorted(couters, key=compare_third_element, reverse=True) 
    corners = []
    for couter in couters:
        if len(corners)==0 or judge(corners, couter):
            corners.append(couter[:2])
        if len(corners)==4:
            break
    return np.array(corners)

def find_one_corner(corners, point):
    point = np.array(point)
    def dis(item):
        return sum((item-point)**2)
    corners = sorted(corners, key=dis)
    return corners[0]

def find_one_edge(edges, corner1, corner3, up1, corner2, corner4, up2):
    edge = np.zeros_like(edges, dtype=bool)
    m1 = (corner1[1]-corner3[1])/(corner1[0]-corner3[0])
    m2 = (corner2[1]-corner4[1])/(corner2[0]-corner4[0])
    height, width = edges.shape
    for x in range(width):
        for y in range(height):
            if edges[y,x] == False:
                continue
            if ((y-corner1[1]-m1*(x-corner1[0])>=0) == up1) and ((y-corner2[1]-m2*(x-corner2[0])>=0) == up2):
                edge[y,x] = True
    return edge

def get_coordinate_list(edge):
    coordinate_list = []
    height, width = edge.shape
    for x in range(width):
        for y in range(height):
            if edge[y,x] == False:
                continue
            coordinate_list.append([y,x])
    return np.array(coordinate_list)

def find_sides(background, mask):
    corners = find_corners(mask)
    edges = cv2.Canny(mask, 100, 200)
    # 点：左上，右上，右下，左上
    corner1 = find_one_corner(corners,[0, 0])
    corner2 = find_one_corner(corners,[background.shape[1], 0])
    corner3 = find_one_corner(corners,[background.shape[1],background.shape[0]])
    corner4 = find_one_corner(corners,[0, background.shape[0]])
    # 边：上、右、下、左
    edge1 = find_one_edge(edges, corner1, corner3, False, corner2, corner4, False)
    edge2 = find_one_edge(edges, corner1, corner3, False, corner2, corner4, True)
    edge3 = find_one_edge(edges, corner1, corner3, True, corner2, corner4, True)
    edge4 = find_one_edge(edges, corner1, corner3, True, corner2, corner4, False)
    edge1_coordinate_list = get_coordinate_list(edge1)
    edge2_coordinate_list = get_coordinate_list(edge2)
    edge3_coordinate_list = get_coordinate_list(edge3)
    edge4_coordinate_list = get_coordinate_list(edge4)
    #上边，y关于x的函数
    edge1_coordinate_list = get_coordinate_list(edge1)
    x = edge1_coordinate_list[:,1]
    y = edge1_coordinate_list[:,0]
    coefficients1 = np.polyfit(x, y, 2)
    #右边，x关于y的函数
    x = edge2_coordinate_list[:,1]
    y = edge2_coordinate_list[:,0]
    coefficients2 = np.polyfit(y, x, 2)
    #下边，y关于x的函数
    x = edge3_coordinate_list[:,1]
    y = edge3_coordinate_list[:,0]
    coefficients3 = np.polyfit(x, y, 2)
    #左边，x关于y的函数
    x = edge4_coordinate_list[:,1]
    y = edge4_coordinate_list[:,0]
    coefficients4 = np.polyfit(y, x, 2)
    return coefficients1, coefficients2, coefficients3, coefficients4

def find_range(mask):
    min_x, max_x, min_y, max_y = None, None, None, None
    height, width = mask.shape
    for x in range(width):
        for y in range(height):
            if mask[y,x]:
                min_x=x
                break
        if min_x:
            break
    
    for x in range(width-1,-1,-1):
        for y in range(height):
            if mask[y,x]:
                max_x=x
                break
        if max_x:
            break
    
    for y in range(height):
        for x in range(width):
            if mask[y,x]:
                min_y=y
                break
        if min_y:
            break
    
    for y in range(height-1,-1,-1):
        for x in range(width):
            if mask[y,x]:
                max_y=y
                break
        if max_y:
            break
    return [min_y, max_y], [min_x, max_x]
    

def find_intersection(coefficients1, coefficients2, y_range, x_range):
    a, b, c = coefficients1
    d, e, f = coefficients2
    delta_x = x_range[1]-x_range[0]+1
    
    for x in range(x_range[0], x_range[1]+1, 1):
        y = a*x*x+b*x+c
        x2 = d*y*y+e*y+f
        if delta_x > abs(x-x2) and y>=y_range[0] and y<=y_range[1]:
            delta_x = abs(x-x2)
            ans_y = int(y)
            ans_x = int(x)
    return [ans_y, ans_x]
    

def find_background_areas(background, mask, erea=[0,0], height_num=4, width_num=4):
    y_range, x_range = find_range(mask)
    
    assert erea[0]>=0 and erea[0]<height_num
    assert erea[1]>=0 and erea[1]<width_num
    
    coefficients1, coefficients2, coefficients3, coefficients4 = find_sides(background, mask)
    small_coefficients1 = erea[0]*(coefficients3-coefficients1)/height_num+coefficients1
    small_coefficients3 = (erea[0]+1)*(coefficients3-coefficients1)/height_num+coefficients1
    small_coefficients4 = erea[1]*(coefficients2-coefficients4)/width_num+coefficients4
    small_coefficients2 = (erea[1]+1)*(coefficients2-coefficients4)/width_num+coefficients4
    
    #交点：左上、右上、右下、左上
    small_corner1 = find_intersection(small_coefficients1, small_coefficients4, y_range, x_range)
    small_corner2 = find_intersection(small_coefficients1, small_coefficients2, y_range, x_range)
    small_corner3 = find_intersection(small_coefficients3, small_coefficients2, y_range, x_range)
    small_corner4 = find_intersection(small_coefficients3, small_coefficients4, y_range, x_range)
    
    return [small_corner1, small_corner2, small_corner3, small_corner4]

def corresponding_projection_all(docs, background, mask, height_num=4, width_num=4):
    result = np.full_like(background, 255)
    for i in range(height_num):
        for j in range(width_num):
            erea = [i,j]
            background_corners = find_background_areas(background, mask, erea, height_num, width_num)
            docs_erea = find_docs_areas(docs, erea, height_num, width_num)
            pts1 = np.float32([[0, 0], [docs_erea.shape[1], 0], [docs_erea.shape[1], docs_erea.shape[0]], [0, docs_erea.shape[0]]])
            pts2 = np.float32([[i[1],i[0]] for i in background_corners])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            transformed_image = cv2.warpPerspective(docs_erea, M, (background.shape[1], background.shape[0]), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
            result = cv2.bitwise_and(result, transformed_image)
            print(f'{(i*width_num+j+1)/height_num/width_num*100}%')
    plt.imshow(result)
    return result

