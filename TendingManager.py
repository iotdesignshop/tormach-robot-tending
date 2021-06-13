import LoadingArray.LoadingArray as LoadingArray
import TendingExceptions
import logging


class TendingManager:
    """TendingManager is the core object you instantiate to manage the tending processes in the system"""
    def __init__(self):
        self.loadingArray = LoadingArray.LoadingArray()

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