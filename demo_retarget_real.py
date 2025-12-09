import numpy as np
import time

import sys

sys.path.append("libgex2")

from libgex import Hand, Glove


from retargeting.gex_retarget import GexRetarget

gex_retarget = GexRetarget()


hand = Hand(port='/dev/ttyUSB0')  # or using port='COMx'
hand.connect()


glove = Glove(port='/dev/ttyACM0')  # or using port='COMx'
glove.connect()

print('start retargeting...')

while True:

    glove_base_pose = np.array([0, 0, 0])

    glove_finger1_pos, glove_finger2_pos, glove_finger3_pos = glove.fk()

    glove_fingers_pos = np.concatenate(
        [
            glove_base_pose[None, :],
            glove_finger1_pos[None, :],
            glove_finger2_pos[None, :],
            glove_finger3_pos[None, :],
        ],
        axis=0,
    )

    qpos = gex_retarget.retarget(glove_fingers_pos)

    print(qpos)

    qpos_degree = qpos * 180 / np.pi

    hand.setj(qpos_degree)

    # time.sleep(1.0 / 240.0)
