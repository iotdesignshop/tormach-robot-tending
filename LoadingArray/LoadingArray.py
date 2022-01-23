from LoadingArray import LoadingArrayItem
import TendingExceptions


class LoadingArray:
    """
    LoadingArray object contain a list of LoadingArrayItem objects that are intended to
    be operated on in sequential order. In addition to a container for those items,
    it provides basic status and management operations.
    """

    def __init__(self):
        self.items = []

    def add_item(self, itemname, pickcoord, placecoord=None):
        """
        Inserts a new item for processing into the LoadingArray
        :param itemname: Unique identifier
        :param pickcoord: Position to pick up the item from
        :param placecoord: Position to return the item to after processing
        :return: LoadingArrayItem object that was just created
        """
        # Ensure itemname is unique
        for checkMe in self.items:
            if checkMe.itemID == itemname:
                raise TendingExceptions.ItemException("Duplicate item name provided for item - they must be unique")

        # Add the item
        item = LoadingArrayItem.LoadingArrayItem(itemname, pickcoord, placecoord)
        self.items.append(item)
        return item

    def get_stats(self):
        """
        Retrieve current statistics about the number of items in the array
        and their processing status.
        :return: { 'total' : Total count of items, 'raw' : Count of unprocessed items, 'processed' : Count of processed
        items, 'error' : Count of items in error state }
        """
        response = {'total': 0, 'raw': 0, 'processed': 0, 'error': 0}
        for item in self.items:
            response["total"] = response["total"] + 1
            if item.state == 'raw':
                response["raw"] = response["raw"] + 1
            elif item.state == 'processed':
                response["processed"] = response["processed"] + 1
            elif item.state == 'error':
                response["error"] = response["error"] + 1
        return response
