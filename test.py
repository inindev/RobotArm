#
# test.py
#
#   copyright 2017 John Clark, apache 2.0 license
#   https://www.apache.org/licenses/LICENSE-2.0
#

import RobotArm


arm = RobotArm()


for i in range(5):
    arm.light.on(100)
    arm.light.sleep_ms(100)


arm.shoulder.up()

arm.grip.open()
arm.grip.sleep_ms(800)
arm.grip.open.stop()

arm.grip.close()
arm.grip.sleep_ms(800)
arm.grip.close.stop()

arm.grip.open()
arm.grip.sleep_ms(800)
arm.grip.open.stop()

arm.grip.close()
arm.grip.sleep_ms(800)
arm.grip.close.stop()

arm.shoulder.up.stop()
