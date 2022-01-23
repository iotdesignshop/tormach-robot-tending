import logging

from WorkflowSteps import MultiGripUtil


class JawPlaceStep:
    """
    The JawPlaceStep is a workflow step which will tell the robot to put a set of jaws onto a VersaBuilt vise
    """

    def __init__(self, vise_position):
        """
        Constructor - set up a jaw pick operation
        :param vise_position: Name of a global pose position specifying the engagement point on the vise
        """
        self.vise_position = vise_position

    def execute_step(self):
        """
        Executes this workflow step which will place the vise jaws onto the MultiGrip vise
        :return: True on success, False on failure
        """
        # Pick up the jaws
        try:
            MultiGripUtil.place_od_jaws(self.vise_position)
            return True
        except Exception as ex:
            logging.error("JawPlaceStep: Execution error " + ex.message)
            return False



