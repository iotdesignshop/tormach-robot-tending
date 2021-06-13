import logging

class MillMDIOperation:

    def __init__(self, mdi_command):
        self.mdi_command = mdi_command

    def execute_step(self):
        logging.info("MillMDIOperation: Executing "+self.mdi_command)
        return True