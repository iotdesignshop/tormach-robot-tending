import logging

class PlaceFinishedPart:

    def __init__(self, parent):
        self.parent = parent

    def execute_step(self):
        logging.info("Placing part - " + self.parent.current_item.itemID)
        return True

