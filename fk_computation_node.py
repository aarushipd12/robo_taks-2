#importing ros2 client library for python. it allows writing ros2 nodes, publishers & subscribers, manage parameters, etc
import rclpy

#importing Node class from ros2 client library
from rclpy.node import Node

#importing Point type msg for 3D coordinates
from geometry_msgs.msg import Point

#numpy importing is reqd for creating and operating matrices
import numpy as np

#forward kinematics class that inherits from parent Node class
class fkNode(Node):
	def __init__(self):
		super().__init__('fk_computation_node')		#initializes node with name 'fk_computation_node'
		
		#declaring parameters for 4 joint angles (the robotic arm has 4 links), setting default values to 0.0
		#namespace='' signifies that parameters are global and ensures no clashing of names occurs.
		self.declare_parameters(namespace='', parameters=[
			('j1', 0.0),
			('j2', 0.0),
			('j3', 0.0),
			('j4', 0.0)
		])	 
		
		#node will publish msgs of type Point to the /robot_fk/end_effector_pose topic
		self.publisher_ = self.create_publisher(Point, '/robot_fk/end_effector_pose', 10)
		
		#self.timer_callback will be called every 1 sec
		self.timer = self.create_timer(1.0, self.timer_callback)
		
		#The robotic arm has 4 links, each of length 1 meter.
		self.link_length = 1.0
		
	#rotation matrices for z-y-x axes.
	def rotation_z(self, theta):
		return np.array([
			[np.cos(theta), -np.sin(theta), 0, 0],
            		[np.sin(theta), np.cos(theta), 0, 0],
            		[0, 0, 1, 0],
            		[0, 0, 0, 1]
            	])
            	
	def rotation_y(self, theta):
		return np.array([
			[np.cos(theta), 0, np.sin(theta), 0],
            		[0, 1, 0, 0],
            		[-np.sin(theta), 0, np.cos(theta), 0],
            		[0, 0, 0, 1]
            	])
            	
	def rotation_x(self, theta):
		return np.array([
			[1, 0, 0, 0],
            		[0, np.cos(theta), -np.sin(theta), 0],
            		[0, np.sin(theta), np.cos(theta), 0],
            		[0, 0, 0, 1]
            	])
            	
        #translation matrix that handles movement along x axis    	
	def translation_x(self, a):
        	return np.array([
			[1, 0, 0, a],
            		[0, 1, 0, 0],
            		[0, 0, 1, 0],
            		[0, 0, 0, 1]
            	])
        #All joints are revolute. Each joint axis is perpendicular to the previous one,  	
	def compute_fk(self):
        	angles = [
        		self.get_parameter('j1').value,
        		self.get_parameter('j2').value,
        		self.get_parameter('j3').value,
        		self.get_parameter('j4').value
        	]
        	
        	#transformation matrices for each joint
        	# @ denotes linkage, or mathematically it is used for matrix multiplication here
        	T1 = self.rotation_z(angles[0]) @ self.translation_x(self.link_length)
        	T2 = self.rotation_y(angles[1]) @ self.translation_x(self.link_length)
        	T3 = self.rotation_x(angles[2]) @ self.translation_x(self.link_length)
        	T4 = self.rotation_y(angles[3]) @ self.translation_x(self.link_length)
        	
        	#combined transformation matrix
        	T_combined = T1 @ T2 @ T3 @ T4
        	return T_combined[:3, 3]
		
	def timer_callback(self):
        	position = self.compute_fk()
        	msg = Point()
        	msg.x, msg.y, msg.z = position
        	self.publisher_.publish(msg)
        	self.get_logger().info(f'End effector position: x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}')		#logs position to console
        
def main(args=None):
	rclpy.init(args=args)
	node = fkNode()			#creates node instance
	rclpy.spin(node)		# .spin() function keeps the node running, executes timer callbacks, etc
	node.destroy_node()
	rclpy.shutdown()		#exit condition for .spin() function	

#ensures main() only runs when script is executed directly	
if __name__ == '__main__':
	main()
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
        		
