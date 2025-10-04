from .Heart import HeartController
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from .PidController import PIDController 
import numpy as np
from .PointsTransformer import transform_points 
import math
class MoveToPointsNode(Node):
    def __init__(self):
        super().__init__('turtle_heart')
        self.get_logger().info("Hello from turtle heart")
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.distance_pid = PIDController(kp=1.5, ki=0, kd=0.01)
        self.angle_pid = PIDController(kp=7, ki=0, kd=0.05)
        self.center_point = np.array([5.5, 5.5])

        self.current_pose = Pose()
        self.current_pose.x = self.center_point[0]
        self.current_pose.y = self.center_point[1]

        self.pose_subcription = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.timer_period = 0.01
        self.timer_ = self.create_timer(self.timer_period, self.timer_callback)
        self.points_generator = self.get_all_generated_points()
        self.distance_tolerance = 0.15

        self.target_point = self.center_point
        self.update_target_point()
    def get_all_generated_points(self):
        yield from transform_points(HeartController().generate_points(), -45)
        yield from transform_points(HeartController().generate_points(), 45)
        yield from transform_points(HeartController().generate_points(), 135)
        yield from transform_points(HeartController().generate_points(), 225)
    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
    def update_target_point(self):
        try:
            self.target_point = next(self.points_generator) + self.center_point
            self.get_logger().info(f"target_point update to: {self.target_point}")
        except StopIteration:
            return
    def pose_callback(self, pose):
        self.current_pose = pose
    def timer_callback(self):
        msg = Twist()
        self.get_logger().info(f"pose: [{self.current_pose.x}, {self.current_pose.y}]")
        dx = self.target_point[0] - self.current_pose.x 
        dy = self.target_point[1] - self.current_pose.y 
        distance = math.sqrt(dx**2 + dy**2)
        self.get_logger().info(f"distance: {distance}")
        # set angle
        target_angle = math.atan2(dy, dx)
        self.get_logger().info(f"target_angle: {target_angle}")
        angle_error = self.normalize_angle(target_angle - self.current_pose.theta)
        self.get_logger().info(f"angle_error: {angle_error}")
        output_w = self.angle_pid.compute(angle_error)
        self.get_logger().info(f"pid output_w: {output_w}")
        msg.angular.z = -output_w


        if distance < self.distance_tolerance:
            self.get_logger().info(f"到达目标点: ({self.current_pose.x}, {self.current_pose.y})")
            self.update_target_point()
            return 
    
        output_v = self.distance_pid.compute(distance) 
        self.get_logger().info(f"pid output_v: {output_v}")
        Kvec = 0.5 # 速度系数
        msg.linear.x = -output_v * Kvec
        self.publisher_.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node = MoveToPointsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stopmsg = Twist()
        node.publisher_.publish(stopmsg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

