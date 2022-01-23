import datetime


class LoadingArrayItem:
    """LoadingArrayItem is the building block for items (typically raw stock) that are added to a LoadingArray
    They have a name and locations where they are to be picked up from to be processed and placed
    after processing (optional - default is to return to the pick position).

    Attributes
    ----------
    itemID : str
        A unique identifier for this specific item

    pickCoordinate : [float, float, float]
        XYZ pick position of this object in loading area

    placeCoordinate : [float, float, float]
        XYZ place position of this object following processing (None = return to pickCoordinate)

    state : "raw", "processed", "error"
        Current processing state of the item

    processingNote: str
        If item has been processed, or processing has resulted in an error, this string will
        describe what happened
    """

    def __init__(self, name, pickcoord, placecoord=None):
        """
        :param name: Unique identifier for the item
        :param pickcoord: XYZ location to pick it up from
        :param placecoord: XYZ location to return it to after processing or None to return to pick location
        """
        self.itemID = name
        self.pickCoordinate = pickcoord
        self.placeCoordinate = placecoord
        self.state = "raw"
        self.processingNote = None

    def is_raw(self):
        """
        Used to check if an item is in raw state (ready for processing)
        :return: True if the item is raw, False if it has been processed, or in an error state
        """
        return self.state == "raw"

    def mark_processed(self):
        """
        Used to mark the item as having been successfully processed
        :return: None
        """
        self.state = "processed"
        self.processingNote = "Processing completed at: " + datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")

    def mark_error(self, errordesc):
        """
        Used to mark the item as having a processing error
        :param errordesc: Description of error that occured
        :return: None
        """
        self.state = "error"
        self.processingNote = errordesc
