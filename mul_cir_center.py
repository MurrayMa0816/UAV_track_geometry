import math
import random
import matplotlib.pyplot as plt
import numpy as np
from sympy import jacobi, jacobi_poly
from graham_scan import graham_scan
# from matplotlib.patches import Ellipse, Circle
class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

class Circle_T:
    def __init__(self, radius, center):
       self.radius = radius
       self.center = center
    #基于圆心角求圆上一点坐标
    def point_on_circle(self, angle_theta): 
        on_circle_x = self.center.X + math.cos(angle_theta) * self.radius
        on_circle_y = self.center.Y + math.sin(angle_theta) * self.radius
        point = Point(int(on_circle_x), int(on_circle_y))
        return point

# # 分别计算两个向量的模：
# l_x=np.sqrt(x.dot(x))
# l_y=np.sqrt(y.dot(y))
# print('向量的模=',l_x,l_y)

# # 计算两个向量的点积
# dian=x.dot(y)
# print('向量的点积=',dian)

# # 计算夹角的cos值：
# cos_=dian/(l_x*l_y)
# print('夹角的cos值=',cos_)

# # 求得夹角（弧度制）：
# angle_hu=np.arccos(cos_)
# print('夹角（弧度制）=',angle_hu)

# # 转换为角度值：
# angle_d=angle_hu*180/np.pi
# print('夹角=%f°'%angle_d)




# 两点与X轴夹角
def angle_two_points(point1, point2):
    v1 =np.array([point1.X - point2.X, point1.Y - point2.Y])
    v2 =np.array([1.0, 0.0])
    v1_=np.sqrt(v1.dot(v1))
    v2_=np.sqrt(v2.dot(v2))
    cos_ = v1.dot(v2)/(v1_*v2_)
    angle_hu=np.arccos(cos_)
    if (v1[1] < 0):
       return 2 * np.pi - angle_hu
       
    else:
        return angle_hu
    # print (angle_d)


def distance_two_points(point1, point2):
    return round(math.sqrt((point1.X - point2.X)**2 +(point1.Y - point2.Y)**2), 2) 
def distance_two_array(point1, point2):
    return round(math.sqrt((point1[0] - point2[0])**2 +(point1[1] - point2[1])**2), 2)
def angle_triangle(distance,r1,r2):
    return math.acos((distance**2+r1**2 -r2**2)/(2*distance*r1))


#求两圆交点
def get_Intersection_two_circles(circle1, circle2):
    
    distance = distance_two_points(circle1.center, circle2.center)
    
    if (distance <= 2*circle1.radius):
        angle_r = angle_two_points(circle1.center, circle2.center)
        angle_t = angle_triangle(distance, circle1.radius, circle2.radius )
        p1 = circle2.point_on_circle(angle_r - angle_t)
        p2 = circle2.point_on_circle(angle_r + angle_t)
        if (p1 == p2):
            return p1
        else:
            return p1, p2
    # elif(distance > 2*circle1.radius and distance < circle1.radius):
    else:
        return 0,0

def generate_points(center_x, center_y, mean_radius, sigma_radius, num_points):
    points = []
    for i in range(num_points):
        theta = random.uniform(0, 2*math.pi)
        radius = random.gauss(mean_radius, sigma_radius)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        points.append((round(x ,2),round(y ,2)))
    return np.array(points)

def generate_polons_center(zuobiaoList):
    dingdian = zuobiaoList[0]
    zongFenziX = 0
    zongFenziY = 0
    zongFenmu = 0
    for i in range(1,len(zuobiaoList)-1):
        xia = zuobiaoList[i]
        shang = zuobiaoList[i+1]
        sanjiaoZhixin = [(dingdian[0]+xia[0]+shang[0])/3, (dingdian[1]+xia[1]+shang[1])/3]
        xiaXiangliang = [xia[0]-dingdian[0], xia[1]-dingdian[1]]
        shangXiangliang = [shang[0]-dingdian[0], shang[1]-dingdian[1]]
        sanjiaoMianji = (xiaXiangliang[0]*shangXiangliang[1]-xiaXiangliang[1]*shangXiangliang[0])/2
        zongFenziX += sanjiaoZhixin[0]*sanjiaoMianji
        zongFenziY += sanjiaoZhixin[1]*sanjiaoMianji
        zongFenmu += sanjiaoMianji

    zuobiaoX = round(zongFenziX/zongFenmu, 4)
    zuobiaoY = round(zongFenziY/zongFenmu, 4)
    return zuobiaoX, zuobiaoY





if __name__ == '__main__':

    fig, ax = plt.subplots()
    plt.xlim(0,900)
    plt.ylim(0,900)
    target_info = np.zeros((6, 2))
    target_info = generate_points(400, 400, 300, 30, 30)
    print(target_info)
    point = []
    circle = []
    delete = []


    for i in range(len(target_info)):
        for j in range(len(target_info)):
            if(i != j):
                print(target_info[i,:],target_info[j,:])
                print(distance_two_array(target_info[i,:],target_info[j,:]))
                if(distance_two_array(target_info[i,:],target_info[j,:]) <40.0):
                    if j not in delete:
                        delete.append(j)
    delete.sort(reverse = True)
    for i in range(len(delete)):
        target_info = np.delete(target_info, delete[i], axis = 0)

    for i in range(len(target_info)):
            point.append(Point(target_info[i,0],target_info[i,1]))
            circle.append(Circle_T(40.0, point[i])) 
            ax.add_patch(plt.Circle((circle[i].center.X, circle[i].center.Y), circle[i].radius,fill=False),)
            plt.scatter(x=point[i].X, y=point[i].Y, c='g', marker='*')
    
    point_intersection = []
    for i in range(len(circle)):
        for j in range(len(circle)):
            if(i != j):
                p1, p2 = get_Intersection_two_circles(circle[i], circle[j])
                if(p1 != 0 and p2 != 0): 
                    if([p1.X,p1.Y] not in point_intersection and  [p2.X,p2.Y] not in point_intersection):
                        point_intersection.append([p1.X,p1.Y,p2.X,p2.Y])
                        # point_intersection.append([p2.X,p2.Y])
                        plt.scatter(x=p1.X, y=p1.Y, c = 'b', s=10)
                        plt.scatter(x=p2.X, y=p2.Y, c = 'b', s=10)
    point_middle = []
    for i in range(len(point_intersection)):
        point_middle.append([(point_intersection[i][2]+ point_intersection[i][0])/2, (point_intersection[i][3] + point_intersection[i][1])/2] ) 

        plt.scatter(x=point_middle[i][0], y=point_middle[i][1], c = 'r', s=20)
    
    if(len(point_middle) > 2):
        result = graham_scan(point_middle)
        length = len(result)
        
        for i in range(0, length - 1):
            plt.plot([result[i][0], result[i + 1][0]], [result[i][1], result[i + 1][1]], c='r')
        plt.plot([result[0][0], result[length - 1][0]], [result[0][1], result[length - 1][1]], c='r')
        centerx, centery= generate_polons_center(result)
        plt.scatter(x=centerx, y=centerx, c = 'g', s=40)
    
    else:
        print("不能构成凸包")
    # ax.set_aspect('equal', adjustable='datalim')
    ax.set_aspect('equal')
    ax.plot()   
    plt.show()
