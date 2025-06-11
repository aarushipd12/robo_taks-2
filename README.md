# robo_taks-2

Outcomes:  Learnt to-
create a workspace, create a package using colcon build, create a node file and add it to my package, forward kinematics computation of a 4th degree of freedom robotic arm by ros implementation (without the use of D-H parameters, using only rotation matrices).

Node file:
The executable includes importing dependencies- rclpy, python library numpy, geometry_msgs.

It comprises of a class, that inherits from the Node class from rclpy.node, consisting of the init function, functions for the rotation/translation matrices, computational function to compute transformation matrices, and a timer callback function where the final logging of the end effector position occurs. And a main function where the instance is created and a .spin() function is revoked to keep the node running and alive. Finally, a standard line of code that ensures that the main function runs only when script is executed directly.

The contents of the package from "robot_fk_ws/src/forward_kinematics_pkg/" are attached to the repo, which include- license file, package.xml, setup.cfg, setup.py
