import math

class PIDController:
    def __init__(self, kp=2.0, ki=0.1, kd=0.1, goal=0.0, dt=0.1) -> None:
        self.Kp = kp # 比例系数
        self.Ki = ki # 积分系数
        self.Kd = kd # 微分系数

        self.goal = goal
        self.prevErr = 0
        self.integral = 0
        self.dt = dt
        
    def set_goal(self, goal):
        self.goal = goal
        self.integral = 0
        self.prevErr = 0
    
    def compute(self, current):
        error = self.goal - current
        proportional = self.Kp * error

        self.integral += error * self.dt
        self.integral = min(max(self.integral, -100), 100) 
        intergralTerm = self.Ki * self.integral 
        derivative = (error - self.prevErr) / self.dt
        derivativeTerm = self.Kd * derivative 
        
        self.prevErr = error
        return proportional + intergralTerm + derivativeTerm
    
    def reset(self):
        self.prevErr = 0
        self.integral = 0


