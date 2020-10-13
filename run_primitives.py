from robot_saeid import Robot
import numpy as np
import time
from simulation import vrep

is_sim =True
workspace_limits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.4]]) # Cols: min max, Rows: x y z (define workspace limits in robot coordinates)
robot = Robot(is_sim, workspace_limits)


#print ('closing the gripper')
#print ('before moving')
#robot.move_to([0.5, 0.5, 0.5], None)

sim_ret, cup_handle  =vrep.simxGetObjectHandle(robot.sim_client,'Cup',vrep.simx_opmode_blocking)
sim_ret, cup_position = vrep.simxGetObjectPosition(robot.sim_client, cup_handle, -1, vrep.simx_opmode_blocking)
print (cup_position)
robot.move_to(cup_position, None)


'''
for i in range(3):
	robot.close_gripper()
	robot.open_gripper()
	time.sleep(2)
'''