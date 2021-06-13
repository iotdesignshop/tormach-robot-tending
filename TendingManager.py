import LoadingArray.LoadingArray as LoadingArray
import TendingExceptions
import logging


class TendingManager:
    """TendingManager is the core object you instantiate to manage the tending processes in the system"""
    def __init__(self):
        self.loadingArray = LoadingArray.LoadingArray()
        self.workflowSteps = []
        self.preWorkflowSteps = []
        self.postWorkflowSteps = []
        self.current_item = None

    def add_item(self, name, pickcoord, placecoord=None):
        """
        Add an individual item to the list of objects to be processed by the manager.
        :param name: Unique identifier (str) for the item being added
        :param pickcoord: Position to pick up the object from
        :param placecoord: Position to place the object after processing, None = place at pick location
        :return: LoadingArrayItem for the item that was added to the manager, None if the addition failed
        """
        try:
            return self.loadingArray.add_item(name, pickcoord, placecoord)
        except TendingExceptions.ItemException as ex:
            logging.error("Error adding item to Tending Array: "+ex.message)
            return None

    def create_2d_array(self, origin, x_column_offset, y_row_offset, max_columns, max_rows, numitems):
        """
        Automatically lay out a 2D grid of items in the picking area where items be picked and returned to
        the layout grid in the same spots.
        :param origin:  [X,Y,Z] coordinate of top left item in the system
        :param x_column_offset: Distance between items in the grid on the X axis
        :param y_row_offset: Distancee between items in the grid on the Y axis
        :param max_columns: Maximum number of columns on X
        :param max_rows: Maximum number of rows on Y
        :param numitems: Number of items to populate into the grid
        :return: LoadingArray object populated with the items, or None if an error occurrd
        """
        # Perform a basic sanity check on the item count
        if max_rows * max_columns < numitems:
            logging.error("Error creating 2D Array: There are more items than slots available in the grid area")
            return None
        if max_rows <= 0 or max_columns <= 0 or numitems <= 0:
            logging.error("Error creating 2D Array: Invalid item count or column count")
            return None

        # Lay out the grid
        for i in range(numitems):
            row = i/max_columns
            col = i%max_columns
            coord = [origin[0]+col*x_column_offset, origin[1]+row*y_row_offset, origin[2]]
            self.add_item("Grid "+str(row)+","+str(col), coord)

        return self.loadingArray

    def create_3d_stack(self, origin, item_z_height, item_count, drop_zone):
        """
        Automatically lay out a stack of items that have been stacked vertically in a known position
        :param origin: Position of 1st item on stack
        :param item_z_height: Height of each item
        :param item_count: Number of items on the stack
        :param drop_zone: Location to drop finished parts
        :return: LoadingArray object populated with the items, or None if an error occurred
        """
        # Perform basic sanity checks on parameters
        if item_z_height <= 0:
            logging.error("Error creating 3D stack: Item height must be greater than zero")
            return None;
        if item_count <= 0:
            logging.error("Error creating 3D stack: Item count must be greater than zero")

        # Lay out the grid
        for i in range(item_count):
            coord = [origin[0], origin[1], origin[2]+i*item_z_height];
            self.add_item("Item " + str(i), coord, drop_zone)

        return self.loadingArray


    def clear_items(self):
        """
        Clears all items that have been added to the manager for a fresh run
        :return: None
        """
        self.loadingArray = LoadingArray.LoadingArray()

    def add_pre_workflow_step(self,workflow_step):
        """
        Adds a workflow step to be executed prior to the main item loop
        :param workflow_step: Step to be added
        :return: None
        """
        self.preWorkflowSteps.append(workflow_step)

    def add_post_workflow_step(self,workflow_step):
        """
        Adds a workflow step to be executed on each item
        :param workflow_step: Step to be added
        :return: None
        """
        self.postWorkflowSteps.append(workflow_step);

    def add_workflow_step(self,workflow_step):
        """
        Adds a workflow step to be executed on each item
        :param workflow_step: Step to be added
        :return: None
        """
        self.workflowSteps.append(workflow_step)

    def clear_workflow_steps(self):
        """Clears the list of workflow steps to prepare for a new sequence of operations"""
        self.workflowSteps = []
        self.preWorkflowSteps = []
        self.postWorkflowSteps = []

    def execute_workflow(self):
        """Commence processing all registered workflow steps and items"""

        # First step - run through pre-workflow
        logging.info("Workflow: Executing Pre-Workflow Steps")
        for step in self.preWorkflowSteps:
            if not step.execute_step():
                # Hit an error or a stop - bail out
                logging.error("Execution failed in Pre-Workflow Step #"+str(self.preWorkflowSteps.index(step)))
                return False

        # Then, run through all items
        logging.info("Workflow: Executing Per-Item Steps")
        for item in self.loadingArray.items:
            self.current_item = item
            for step in self.workflowSteps:
                if not step.execute_step():
                    # Hit an error or a stop - bail out
                    logging.error("Execution failed in workflow Step #{0} ({2}) on Item #{1} ({3})"
                                  .format(str(self.workflowSteps.index(step)),
                                          str(self.loadingArray.items.index(item)),
                                          step.__class__.__name__,
                                          item.itemID))
                    item.mark_error("Execution failed in workflow Step#{0} ({1})",
                                    str(self.workflowSteps.index(step)),
                                    step.__class__.__name__)
                    return False
                else:
                    item.mark_processed()

            logging.info(self.loadingArray.get_stats())


        # Final step - run through post-workflow
        logging.info("Workflow: Executing Post-Workflow Steps")
        for step in self.postWorkflowSteps:
            if not step.execute_step():
                # Hit an error or a stop - bail out
                logging.error("Execution failed in Post-Workflow Step #"+str(self.postWorkflowSteps.index(step)))
                return False
