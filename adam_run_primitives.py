from robot_saeid import Robot
import numpy as np
import time
from simulation import vrep


is_sim =True
workspace_limits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.4]]) # Cols: min max, Rows: x y z (define workspace limits in robot coordinates)
robot = Robot(is_sim, workspace_limits)

#Variables Adam made
heightmap_rotation_angle = 0 #needed for grasp function
workspace_center = [-.5, 0, .02] #where the objects will be placed

#getting handles of objects, will have to be replaced by camera-based positions
blk_handle = [0]*2
blk_position = [0]*2
sim_ret, cup_handle  =vrep.simxGetObjectHandle(robot.sim_client,'Cup',vrep.simx_opmode_blocking)
sim_ret, cup_position = vrep.simxGetObjectPosition(robot.sim_client, cup_handle, -1, vrep.simx_opmode_blocking)
#make sure to uncheck 'static' when making concrete blocks
sim_ret, blk_handle[0]  =vrep.simxGetObjectHandle(robot.sim_client,'ConcretBlock#0',vrep.simx_opmode_blocking)
sim_ret, blk_position[0] = vrep.simxGetObjectPosition(robot.sim_client, blk_handle[0], -1, vrep.simx_opmode_blocking)
sim_ret, blk_handle[1]  =vrep.simxGetObjectHandle(robot.sim_client,'ConcretBlock#1',vrep.simx_opmode_blocking)
sim_ret, blk_position[1] = vrep.simxGetObjectPosition(robot.sim_client, blk_handle[1], -1, vrep.simx_opmode_blocking)
#end of getting handles for objects

#handle of UR5_target, needed as a home for the robotic arm, may want to replace it with the actual starting position of the arm
sim_ret, UR5_target_handle = vrep.simxGetObjectHandle(robot.sim_client,'UR5_target',vrep.simx_opmode_blocking)
sim_ret, UR5_target_position = vrep.simxGetObjectPosition(robot.sim_client, UR5_target_handle, -1, vrep.simx_opmode_blocking)

#testing camera
robot.setup_sim_camera()
rgb, depth = robot.get_camera_data()
#print(rgb)
#print(depth)
#robot.pretrained_torch(rgb)
#end of testing camera


objectsPresent = 2 #planned to be filled with objects detected by cameras
towerTip = workspace_center #tip of tower, where next block will be placed
tipRaise = .05 #how much towerTip must be raised by to properly place next object, will be slightly higher than picked object
for i in range(0, objectsPresent):
	robot.grasp(blk_position[i],heightmap_rotation_angle,workspace_limits, towerTip) # Arm crashes when presented with an impossible grasp
	robot.move_to(UR5_target_position, None)
	towerTip[2] += tipRaise



## start of hard-code pick and place
#above_cup = [cup_position[0],cup_position[1],cup_position[2] + .1]
#side_above_cup = [cup_position[0] - .1,cup_position[1],cup_position[2] + .1]
#side_cup_position = [cup_position[0] - .1,cup_position[1],cup_position[2]]

#print ("above_cup", above_cup)
#time.sleep(2)
#robot.move_to(above_cup, None)
#robot.open_gripper()
#print("cup_position", cup_position)
#robot.move_to(cup_position, None)
#robot.close_gripper()
#robot.move_to(above_cup, None)
#robot.move_to(side_above_cup,None)
#robot.move_to(side_cup_position,None)
#robot.open_gripper()
#robot.move_to(side_above_cup,None)

## end of hard-code pick and place

#ends simulation
robot.restart_sim()
vrep.simxStopSimulation(robot.sim_client,vrep.simx_opmode_oneshot_wait)



'''
for i in range(3):
	robot.close_gripper()
	robot.open_gripper()
	time.sleep(2)
'''