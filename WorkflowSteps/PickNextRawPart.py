import logging

class PickNextRawPart:

    def __init__(self, parent):
        self.parent = parent;

    def execute_step(self):
        # Get position of item
        logging.info("Picking part - "+self.parent.current_item.itemID)
        return True
