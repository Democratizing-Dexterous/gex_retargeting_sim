from dex_retargeting.retargeting_config import RetargetingConfig
from dex_retargeting.seq_retarget import SeqRetargeting
import os

from .custom_constants import (
    get_default_config_path,
    RobotName,
    RetargetingType,
    HandType,
    ROBOT_NAME_MAP_INV,
)

base_dir = os.path.dirname(os.path.abspath(__file__))


class GexRetarget:
    def __init__(self):
        robot_name = ROBOT_NAME_MAP_INV["gx10"]
        retargeting_type = RetargetingType.dexpilot
        hand_type = HandType.right

        config_path = get_default_config_path(robot_name, retargeting_type, hand_type)

        robot_dir = os.path.join(base_dir, "urdf")
        RetargetingConfig.set_default_urdf_dir(str(robot_dir))
        self.retargeting = RetargetingConfig.load_from_file(config_path).build()

        self.task_indices = [2, 3, 3, 0, 0, 0]
        self.origin_indices = [1, 1, 2, 1, 2, 3]

    def retarget(self, finger_pos_list):
        ref_value = (
            finger_pos_list[self.origin_indices, :]
            - finger_pos_list[self.task_indices, :]
        )
        qpos = self.retargeting.retarget(ref_value)
        return qpos
