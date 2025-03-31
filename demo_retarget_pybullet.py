import pybullet as p
import pybullet_data
import numpy as np
import time

from retargeting.gex_retarget import GexRetarget

gex_retarget = GexRetarget()


p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.configureDebugVisualizer(p.COV_ENABLE_Y_AXIS_UP, 1) # Y axis up
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally

p.resetDebugVisualizerCamera(cameraDistance=1.08, cameraYaw=180, cameraPitch=-14.6, cameraTargetPosition=[0.14, -0.1, -0.81])


hand_offset = np.array([0.25, 0, 0])
hand = p.loadURDF("retargeting/urdf/gx11/urdf/gx11.urdf", useFixedBase=True, basePosition=hand_offset)

glove = p.loadURDF("retargeting/urdf/ex12/urdf/ex12.urdf", useFixedBase=True, basePosition=[0, 0, 0])

glove_finger1_id = 4
glove_finger2_id = 9
glove_finger3_id = 14

p.setGravity(0, 0, 0)


# get valid joints
valid_joints = []
for i in range(p.getNumJoints(hand)):
    info = p.getJointInfo(hand, i)
    print(info[1])
    if info[2] == p.JOINT_REVOLUTE:
        
        valid_joints.append(i)


while True:
    
    glove_base_pose = np.array([0, 0, 0])

    # get glove finger positions in xyz
    glove_finger1_pos = np.array(p.getLinkState(glove, glove_finger1_id, computeForwardKinematics=1)[4]) 
    glove_finger2_pos = np.array(p.getLinkState(glove, glove_finger2_id, computeForwardKinematics=1)[4]) 
    glove_finger3_pos = np.array(p.getLinkState(glove, glove_finger3_id, computeForwardKinematics=1)[4])
    
    glove_fingers_pos = np.concatenate([glove_base_pose[None, :], glove_finger1_pos[None, :], glove_finger2_pos[None, :], glove_finger3_pos[None, :]], axis=0)

    qpos = gex_retarget.retarget(glove_fingers_pos)

    for i in range(len(valid_joints)):
        p.setJointMotorControl2(hand, valid_joints[i], p.POSITION_CONTROL, targetPosition=qpos[i])

    p.stepSimulation()

    time.sleep(1./240.)


