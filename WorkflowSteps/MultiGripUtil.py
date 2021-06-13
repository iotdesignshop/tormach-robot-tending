import logging

physical_robot = False

if (physical_robot == True):
    from robot_command.rpl import *

    def open_multigrip():
        set_digital_out("multi_close", False)
        set_digital_out("multi_open", True)

    def close_multigrip():
        set_digital_out("multi_close", True)
        set_digital_out("multi_open", False)

    def float_multigrip():
        set_digital_out("multi_close", False)
        set_digital_out("multi_open", False)

    def close_vise():
        set_digital_out("vise", True)

    def open_vise():
        set_digital_out("vise", False)

    def pick_od_jaws(origin):
        with work_offset(origin):
            # Vise initial state
            close_multigrip()
            close_vise()
            sleep(1)

            # Step 1: Move to 50mm away from vise in Y
            movej(Pose(x=0.0, y=-50.0, z=0.0))

            # Step 2: Engage - move in X until pins engage but dovetails don't
            movej(Pose(x=0, y=-3.5, z=0))

            # Step 3: Side shift to engage dowel pin in fixed side window
            movej(Pose(x=5.1, y=-3.5))

            # Step 4: Open gripper to engage window on moving side
            open_multigrip()
            sleep(1)

            # Step 5: Float gripper, center position of 3 position center exhaust valve
            float_multigrip()
            sleep(1)

            # Step 6: Engage face to face
            movej(Pose(x=5.1, y=0.0))

            # Step 7: Side shift to engage dowel pins
            movej(Pose(x=0, y=0))

            # Step 8: close gripper to engage on jaws
            close_multigrip()
            sleep(1)

            # Step 9: Open vise"
            open_vise()
            sleep(1)

            # Step 10: side shift to clear fixed side dovetail on vise
            movej(Pose(x=-3.9))

            # Step 11: up and away
            movej(Pose(x=-3.9, z=50))

    def place_od_jaws(origin):
        with work_offset(origin):
            # Step 1: Open vise
            open_vise()
            sleep(1)

            # Step 2: Approach above vise
            movej(Pose(x=-3.9, y=0, z=50))

            # Step 3: Engage with vise surface
            movej(Pose(x=-3.9, y=0, z=0))

            # Step 4: Shift to engage fixed side of vise
            movej(Pose(x=0, y=0, z=0))

            # Step 5: Close vise to clamp on jaws
            close_vise()
            open_multigrip()
            sleep(1)

            # Step 6: Shift to release gripper dovetails
            movej(Pose(x=5.1, y=0, z=0))

            # Step 8: Float gripper
            float_multigrip()
            sleep(1)

            # Step 9: Pull away
            movej(Pose(x=5.1, y=-50., z=0))

else:

    logging.basicConfig(level=logging.INFO)

    def open_multigrip():
        logging.info("Simulation Environment: Open Multigrip")

    def close_multigrip():
        logging.info("Simulation Environment: Close Multigrip")

    def float_multigrip():
        logging.info("Simulation Environment: Float Multigrip")

    def close_vise():
        logging.info("Simulation Environment: Close Vise")

    def open_vise():
        logging.info("Simulation Environment: Open Vise")

    def pick_od_jaws(origin):
        logging.info("Simulation Environment: Picked up jaws")

    def place_od_jaws(origin):
        logging.info("Simulation Environment: Placed jaws")
