
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import pygame,sys
from sympy import jacobi, jacobi_poly
from graham_scan import graham_scan
from point_mov import ParticleSimulator
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
# from matplotlib.patches import Ellipse, Circle
class Point:
    def __init__(self, x, y, x_vel, y_vel):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

class Circle_T:
    def __init__(self, radius, center):
       self.radius = radius
       self.center = center
    #基于圆心角求圆上一点坐标
    def point_on_circle(self, angle_theta): 
        on_circle_x = self.center.x + math.cos(angle_theta) * self.radius
        on_circle_y = self.center.y + math.sin(angle_theta) * self.radius
        point = Point(int(on_circle_x), int(on_circle_y), 0 ,0)
        return point


# 两点与X轴夹角
def angle_two_points(point1, point2):
    v1 =np.array([point1.x - point2.x, point1.y - point2.y])
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
    return round(math.sqrt((point1.x - point2.x)**2 +(point1.y - point2.y)**2), 2) 
def distance_two_array(point1, point2):
    return round(math.sqrt((point1[0] - point2[0])**2 +(point1[1] - point2[1])**2), 2)
def angle_triangle(distance,r1,r2):
    return math.acos((distance**2+r1**2 -r2**2)/(2*distance*r1))

track_point = []
zongFenmu_list = []
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
        x_v= random.uniform(15,25)
        y_v= random.uniform(10,12)
        points.append(Point(round(x ,2), round(y ,2), round(x_v ,2), round(y_v ,2) ))
    return points

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
    zongFenmu_list.append((zongFenmu))
    print(zongFenmu_list)
    if zongFenmu == 0:
       zongFenmu = zongFenmu_list[0]
       print("---",zongFenmu)
    else:
        pass
    zuobiaoX = round(zongFenziX/zongFenmu, 4)
    zuobiaoY = round(zongFenziY/zongFenmu, 4)
    zongFenmu_list.pop(0)
    print(zongFenmu_list)

    return zuobiaoX, zuobiaoY

def paint_center(target_info):
    circle = []
    for i in range(len(target_info)):
            circle.append(Circle_T(40.0,target_info[i])) 
            pygame.draw.circle(screen,BLACK,(circle[i].center.x, circle[i].center.y),circle[i].radius, 2)
            pygame.draw.circle(screen,BLACK,(circle[i].center.x, circle[i].center.y),2, 2)
    
    point_intersection = []
    for i in range(len(circle)):
        for j in range(len(circle)):
            if(i != j):
                p1, p2 = get_Intersection_two_circles(circle[i], circle[j])
                if(p1 != 0 and p2 != 0): 
                    if([p1.x,p1.y] not in point_intersection and  [p2.x,p2.y] not in point_intersection):
                        point_intersection.append([p1.x,p1.y,p2.x,p2.y])
                        # point_intersection.append([p2.X,p2.Y])
                        pygame.draw.circle(screen,GREEN,(p1.x, p1.y),4,4)
                        pygame.draw.circle(screen,GREEN,(p2.x, p2.y),4,4)
                      
    point_middle = []
    for i in range(len(point_intersection)):
        point_middle.append([(point_intersection[i][2]+ point_intersection[i][0])/2, (point_intersection[i][3] + point_intersection[i][1])/2] ) 
        pygame.draw.circle(screen,BLUE,(point_middle[i][0], point_middle[i][1]),5,5)
       
    
    
    if(len(point_middle) > 2):
        result = graham_scan(point_middle)
        length = len(result)
        
        for i in range(0, length - 1):
            pygame.draw.line(screen, RED, (result[i][0], result[i][1]),( result[i + 1][0], result[i + 1][1]), 3)
        pygame.draw.line(screen, RED, (result[0][0], result[0][1] ),(result[length - 1][0], result[length - 1][1]), 3)
        centerx, centery= generate_polons_center(result)
        pygame.draw.circle(screen,PURPLE,(centerx, centery),4,4)
        if (len(track_point) == 0):
            track_point.append((centerx, centery))
            track_point.append((centerx, centery))
        else:
            track_point.append((centerx, centery))
        # print(track_point)
        pygame.draw.lines(screen, PURPLE, False, track_point, 3)
        # filter_point = []
        # if(len(track_point) > 3):
        #     if (track_point[0][0] == track_point[1][0]):
        #         track_point.pop(0)
        #     else:
        #         x = np.array(track_point)[:,0]
        #         y = np.array(track_point)[:,1]
        #         print(x,y)
        #         x_smooth = np.linspace(np.array(track_point)[:,0].min(),np.array(track_point)[:,0].max(), 300)  # np.linspace 等差数列,从x.min()到x.max()生成300个数，便于后续插值
        #         y_smooth = make_interp_spline(x, y)(x_smooth)
        #         for m in range(len(x_smooth)):
        #             filter_point.append((x_smooth[m],y_smooth[m]))
        #         pygame.draw.lines(screen, RED, False,filter_point, 3)
            

        # Savitzky-Golay 滤波器实现曲线平滑
        y = savgol_filter(np.array(track_point)[:,1], 133,8, mode= 'nearest')
        filter_point = []
        for m in range(len(y)):
            filter_point.append((track_point[m][0], y[m]))
        pygame.draw.lines(screen, RED, False,filter_point, 3)

    
    else:
        pass
    # return point_intersection, point_middle, 

def valid_target(target_info):
    delete = []
    for i in range(len(target_info)):
        for j in range(len(target_info)):
            if(i != j):
                if(distance_two_points(target_info[i],target_info[j]) <40.0):
                    if j not in delete:
                        delete.append(j)
    delete.sort(reverse = True)
    for i in range(len(delete)):
        target_info.pop(delete[i])
    return target_info



if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((1600,1000))
    screen.fill(WHITE)
    keep_going = True

    clock = pygame.time.Clock()
    target_info = np.zeros((6, 2))
    target_info = generate_points(400, 400, 300, 30, 30)
    target_info = valid_target(target_info)
    target_info_mov = ParticleSimulator(target_info)
    # 游戏循环
    while True:
        for event in pygame.event.get(): # 循环遍历事件
            if event.type == pygame.QUIT:
                sys.exit()
        fps = clock.get_fps()  # 获取游戏帧率    
        print(fps)
        screen.fill((255,255,255))
        target_info_mov.evolve(0.1)
        paint_center(target_info_mov.particles)
        pygame.display.update()
        clock.tick(60)
    # 游戏退出
    pygame.quit()



 



  