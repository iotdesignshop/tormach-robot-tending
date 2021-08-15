import TendingManager
import LoadingArray.LoadingArray as LoadingArray
import LoadingArray.LoadingArrayItem as LoadingArrayItem
import WorkflowSteps.JawPickStep as JawPickStep
import WorkflowSteps.JawPlaceStep as JawPlaceStep
import WorkflowSteps.PickNextRawPart as PickNextRawPart
import WorkflowSteps.PlaceFinishedPart as PlaceFinishedPart
import WorkflowSteps.MillMDIOperation as MillMDIOperation


manager = TendingManager.TendingManager()

# Just some rough test data here as a baseline
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

# Test a Basic Workflow
print("====== Testing Workflow Sequence ====== ")

manager.add_pre_workflow_step(JawPickStep.JawPickStep("vise_1_origin"))

manager.add_workflow_step(PickNextRawPart.PickNextRawPart(manager))
manager.add_workflow_step(JawPlaceStep.JawPlaceStep("vise_1_origin"))
manager.add_workflow_step(MillMDIOperation.MillMDIOperation("cut_my_part.nc"))
manager.add_workflow_step(JawPickStep.JawPickStep("vise_1_origin"))
manager.add_workflow_step(PlaceFinishedPart.PlaceFinishedPart(manager))
manager.add_workflow_step(MillMDIOperation.MillMDIOperation("washdown.nc"))

manager.add_post_workflow_step(JawPlaceStep.JawPlaceStep("vise_1_origin"))

manager.execute_workflow()

# Success
print("+++++++++++++++++++++++++++")
print("Test completed successfully");

