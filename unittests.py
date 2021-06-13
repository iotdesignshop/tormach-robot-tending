import TendingManager
import LoadingArray.LoadingArray as LoadingArray
import LoadingArray.LoadingArrayItem as LoadingArrayItem

manager = TendingManager.TendingManager()

origin = [100, 200, 9]
xoff = 87
yoff = 123
numcol = 4
numrow = 3
count = 10

# Test Expected Case - Construct a valid 2D grid
print("====== Testing 2D Grid ====== ")
loading = manager.create_2d_array(origin, xoff, yoff, numcol, numrow, count)

for item in loading.items:
    idx = loading.items.index(item)
    row = idx / numcol
    col = idx % numcol
    print("Name:{0} Pick: {1},{2},{3}".format(item.itemID, item.pickCoordinate[0], item.pickCoordinate[1], item.pickCoordinate[2]))
    expectedX = origin[0] + col*xoff
    expectedY = origin[1] + row*yoff
    if (item.pickCoordinate[0] == expectedX) and \
            (item.pickCoordinate[1] == expectedY) and \
            (item.pickCoordinate[2] == origin[2]):
        print("In correct position")
    else:
        print("Position error")
        raise Exception("Position error on item "+str(idx))

manager.clear_items();


# Test Expected Case - Construct a valid 3D stack
print("====== Testing 3D Stack ====== ")

zoff = 24.5
drop = [500, 500, 300]

loading = manager.create_3d_stack(origin, zoff, count, drop)

for item in loading.items:
    idx = loading.items.index(item)
    print("Name:{0} Pick: {1},{2},{3}".format(item.itemID, item.pickCoordinate[0], item.pickCoordinate[1], item.pickCoordinate[2]))
    expectedZ = origin[2] + idx * zoff

    if (item.pickCoordinate[0] == origin[0]) and \
            (item.pickCoordinate[1] == origin[1]) and \
            (item.pickCoordinate[2] == expectedZ):
        print("In correct position")
    else:
        print("Position error")
        raise Exception("Position error on item "+str(idx))

# Success
print("+++++++++++++++++++++++++++")
print("Test completed successfully");

