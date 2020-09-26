from robot_saeid import Robot
import numpy as np
import time
is_sim =True
workspace_limits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.4]]) # Cols: min max, Rows: x y z (define workspace limits in robot coordinates)
robot = Robot(is_sim, workspace_limits)


print ('closing the gripper')
robot.move_to([-0.1, 0, 0.3], None)
'''
for i in range(3):
	robot.close_gripper()
	robot.open_gripper()
	time.sleep(2)
'''