import math
import matplotlib.pyplot as plt
import numpy as np
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
        point = Point(on_circle_x, on_circle_y)
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
    return math.sqrt((point1.X - point2.X)**2 +(point1.Y - point2.Y)**2)

def angle_triangle(distance,r1,r2):
    return math.acos((distance**2+r1**2 -r2**2)/(2*distance*r1))


#求两圆交点
def get_Intersection_two_circles(circle1, circle2):
    
    distance = distance_two_points(circle1.center, circle2.center)
    if (distance <= 2*circle1.radius):
        angle_r = angle_two_points(circle1.center, circle2.center)
        angle_t = angle_triangle(distance, circle1.radius, circle2.radius )
        p1 = circle2.point_on_circle(angle_r - angle_t)
        p2 = Circle2.point_on_circle(angle_r + angle_t)
        if (p1 == p2):
            return p1
        else:
            return p1, p2
    elif(distance > 2*circle1.radius & distance < circle1.radius):
        return 0

if __name__ == '__main__':

    point1 = Point(8, 8)
    point2 = Point(10, 10)
    Circle1 = Circle_T(3,point1)
    Circle2 = Circle_T(3,point2)
    p1, p2 = get_Intersection_two_circles(Circle1, Circle2)
    print(p1.X, p2.X)

    fig, ax = plt.subplots()
    ax.add_patch(plt.Circle((Circle1.center.X,Circle1.center.Y),Circle1.radius,fill=False))
    ax.add_patch(plt.Circle((Circle2.center.X,Circle2.center.Y),Circle1.radius,fill=False))
    plt.scatter(x=p1.X, y=p1.Y)
    plt.scatter(x=p2.X, y=p2.Y)

    ax.set_aspect('equal', adjustable='datalim')
    ax.plot()   
    plt.show()

# patches=[]      #创建容纳对象的集合

# patches.append(e1)   #将创建的形状全部放进去

# patches.append(e2)

# collection=PatchCollection(patches)  #构造一个Patch的集合

# ax.add_collection(collection)    #将集合添加进axes对象里面去

# plt.show() #最后显示图片即可