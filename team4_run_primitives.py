from robot_saeid import Robot
import numpy as np
import time
from simulation import vrep
from PIL import Image
import detect

#Setup
is_sim =True
workspace_limits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.4]]) # Cols: min max, Rows: x y z (define workspace limits in robot coordinates)
robot = Robot(is_sim, workspace_limits)

#Variable Creation
heightmap_rotation_angle = 0 #needed for grasp function
workspace_center = [-.5, 0, .03] #where the objects will be placed

#Handle of UR5_target, needed as a home for the robotic arm
sim_ret, UR5_target_handle = vrep.simxGetObjectHandle(robot.sim_client,'UR5_target',vrep.simx_opmode_blocking)
sim_ret, UR5_target_position = vrep.simxGetObjectPosition(robot.sim_client, UR5_target_handle, -1, vrep.simx_opmode_blocking)

#Camera With YOLOv5
robot.setup_sim_camera()
rgb, depth = robot.get_camera_data()
workspace_picture = Image.fromarray(rgb)
workspace_picture.save("/home/saeid/Downloads/CoppeliaSim_Edu_V4_1_0_Ubuntu18_04/programming/remoteApiBindings/python/python/data/images/workspace.jpg")

#Detect number of objects
objectsPresent = detect.detect(False) #filled with objects detected by cameras
objectsPresent = int(objectsPresent)
print("Number of Objects detected: ", objectsPresent)
towerTip = workspace_center #tip of tower, where next block will be placed
tipRaise = .06 #how much towerTip must be raised by to properly place next object, slightly taller than picked object

#Make list of objects in workspace
cyl_handle = [0]*objectsPresent
cyl_position = [0]*objectsPresent
for j in range(0, objectsPresent):
	name = ('Cylinder#%d' % j)
	sim_ret, cyl_handle[j]  =vrep.simxGetObjectHandle(robot.sim_client,name,vrep.simx_opmode_blocking)
	sim_ret, cyl_position[j] = vrep.simxGetObjectPosition(robot.sim_client, cyl_handle[j], -1, vrep.simx_opmode_blocking)


for i in range(0, objectsPresent): #execute each grasp for each object
	robot.grasp(cyl_position[i],heightmap_rotation_angle,workspace_limits, towerTip)
	robot.move_to(UR5_target_position, None)
	towerTip[2] += tipRaise

#End simulation
robot.restart_sim()
vrep.simxStopSimulation(robot.sim_client,vrep.simx_opmode_oneshot_wait)

