#
# test.py
#
#   copyright 2017 John Clark, apache 2.0 license
#   https://www.apache.org/licenses/LICENSE-2.0
#

import robotarm


robot_arm = RobotArm()


for i in range(5):
    robot_arm.light.on(100)
    robot_arm.light.sleep_ms(100)


robot_arm.shoulder.up()

robot_arm.grip.open()
robot_arm.grip.sleep_ms(800)
robot_arm.grip.open.stop()

robot_arm.grip.close()
robot_arm.grip.sleep_ms(800)
robot_arm.grip.close.stop()

robot_arm.grip.open()
robot_arm.grip.sleep_ms(800)
robot_arm.grip.open.stop()

robot_arm.grip.close()
robot_arm.grip.sleep_ms(800)
robot_arm.grip.close.stop()

robot_arm.shoulder.up.stop()

