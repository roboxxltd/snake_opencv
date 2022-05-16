import cv2
import random
import math

from sympy import false, true
class Snake:
    body_point = []
    head_point = [0, 0]
    head_width = 25
    body_width = 15
    body_length = 1
    food_width = 20
    food_position = [100, 100]
    game = 0
    def __init__(self, width = 640):
        print("初始化蛇")
        self.head_width = int(width * 0.025)
        self.body_width = int(width * 0.020)
        self.food_width = int(width * 0.030)
        if self.food_width < 20:
            self.food_width = 20
        if self.head_width < 25:
            self.head_width = 25
        if self.body_width < 15:
            self.body_width = 15
        

    # 蛇头的位置
    def head_coordinate(self, frame, center):
        cv2.putText(frame, str(self.body_length - 1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, ), 3)
        if self.distance(self.head_point, center) > self.body_width:
            self.head_point = center
            self.body_point.append(self.head_point)
        self.eat_food(frame)
        self.delete_body()
        self.draw_body(frame)
        if self.check_head():
            self.game = 1
    

    def distance(self, a, b):
        return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))

    # 判断是否吃到食物
    def eat_food(self, frame):
        if self.distance(self.food_position, self.head_point) < self.head_width:
            self.add_body()
            self.randomly_generated_food(frame)

    # 判断是否撞到身子
    def check_head(self):
        for i in range(0, self.body_length -2):
            if self.distance(self.head_point, self.body_point[i]) < self.body_width - 3:
                return true
        return false

    # 检查食物与蛇是否重合
    def check_food(self):
        for body in self.body_point:
            if self.distance(self.food_position, body) < self.body_width:
                return true
        return false

    # 随机生成食物
    def randomly_generated_food(self, frame):
        # 1280 / 10 // 800 / 10
        size = frame.shape
        x = random.randint(size[1]*0.2, int(size[1]) - size[1]*0.2)
        y = random.randint(size[0]*0.2, int(size[0]) - size[0]*0.2)
        self.food_position = [x, y]

        while self.check_food():
            x = random.randint(0, int(size[1]))
            y = random.randint(0, int(size[0]))
            self.food_position = [x, y]
        
    # 添加身体长度
    def add_body(self):
        self.body_length += 1

    # 判断列表数据是否超过身体长度
    def delete_body(self):
        while self.body_length < len(self.body_point):
            self.body_point.pop(0)

    def draw_body(self, draw_img):
        cv2.circle(draw_img, self.head_point, self.head_width, (0, 255, 0), -1)
        # for body in self.body_point:
        if self.body_length > 1:
            for i in range(0, self.body_length - 1):
            # print(body)
                cv2.circle(draw_img, self.body_point[i], self.body_width, (100, 250, 0), -1)
        cv2.circle(draw_img, self.food_position, self.food_width, (0, 0, 255), -1)
