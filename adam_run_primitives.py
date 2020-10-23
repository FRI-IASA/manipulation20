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


#sim_ret, test = vrep.simxGetObjectOrientation(robot.sim_client, cup_handle, -1, vrep.simx_opmode_blocking)

#robot.setup_sim_camera()
#sim_ret, test2 = robot.get_camera_data()

#test1, test2, tes3, bes1, test = vrep.simxGetObjectGroupData(robot.sim_client, cup_handle, 4, vrep.simx_opmode_blocking)
#print(test2)

#robot.guarded_move_to(cup_position, test)

## start of hard-code pick and place
above_cup = [cup_position[0],cup_position[1],cup_position[2] + .1]
side_above_cup = [cup_position[0] - .1,cup_position[1],cup_position[2] + .1]
side_cup_position = [cup_position[0] - .1,cup_position[1],cup_position[2]]

print ("above_cup", above_cup)
time.sleep(2)
robot.move_to(above_cup, None)
robot.open_gripper()
print("cup_position", cup_position)
robot.move_to(cup_position, None)
robot.close_gripper()
robot.move_to(above_cup, None)
robot.move_to(side_above_cup,None)
robot.move_to(side_cup_position,None)
robot.open_gripper()
robot.move_to(side_above_cup,None)

## end of hard-code pick and place

robot.restart_sim()
vrep.simxStopSimulation(robot.sim_client,vrep.simx_opmode_oneshot_wait)



'''
for i in range(3):
	robot.close_gripper()
	robot.open_gripper()
	time.sleep(2)
'''