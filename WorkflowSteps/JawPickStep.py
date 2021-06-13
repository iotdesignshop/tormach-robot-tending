import logging

import WorkflowStep
import MultiGripUtil


class JawPickStep:
    """
    The JawPickStep is a workflow step which will tell the robot to pick up a set of jaws from a versabuilt vise
    """

    def __init__(self, vise_position):
        """
        Constructor - set up a jaw pick operation
        :param vise_position: Name of a global pose position specifying the engagement point on the vise
        """
        self.vise_position = vise_position

    def execute_step(self):
        """
        Executes this workflow step which will pick up the vise jaws from the MultiGrip vise
        :return: True on success, False on failure
        """
        # Pick up the jaws
        try:
            MultiGripUtil.pick_od_jaws(self.vise_position)
            return True
        except Exception as ex:
            logging.error("JawPickStep: Execution error "+ex.message);
            return False



