#
# robotcmd.py
#
#   copyright 2017 John Clark, apache 2.0 license
#   https://www.apache.org/licenses/LICENSE-2.0
#

import sys
from robotarm import RobotArm


robot_arm = RobotArm()


def blink(repeat=5, ms=100):
    for i in range(repeat):
        robot_arm.light.on(ms)
        robot_arm.light.sleep_ms(ms)


robot_commands = {
    'grip.close': robot_arm.grip.close,
    'grip.close.stop': robot_arm.grip.close.stop,
    'grip.open': robot_arm.grip.open,
    'grip.open.stop': robot_arm.grip.open.stop,

    'wrist.up': robot_arm.wrist.up,
    'wrist.up.stop': robot_arm.wrist.up.stop,
    'wrist.down': robot_arm.wrist.down,
    'wrist.down.stop': robot_arm.wrist.down.stop,

    'elbow.up': robot_arm.elbow.up,
    'elbow.up.stop': robot_arm.elbow.up.stop,
    'elbow.down': robot_arm.elbow.down,
    'elbow.down.stop': robot_arm.elbow.down.stop,

    'shoulder.up': robot_arm.shoulder.up,
    'shoulder.up.stop': robot_arm.shoulder.up.stop,
    'shoulder.down': robot_arm.shoulder.down,
    'shoulder.down.stop': robot_arm.shoulder.down.stop,

    'base.cw': robot_arm.base.cw,
    'base.cw.stop': robot_arm.base.cw.stop,
    'base.ccw': robot_arm.base.ccw,
    'base.ccw.stop': robot_arm.base.ccw.stop,

    'light.off': robot_arm.light.off,
    'light.off.stop': robot_arm.light.off.stop,
    'light.on': robot_arm.light.on,
    'light.on.stop': robot_arm.light.on.stop,

    'blink': blink
}


def invoke_command(name, ms):
    fcn = robot_commands.get(name)
    if fcn == None:
        print('skipping unknown command: {}'.format(name))
        return

    if ms < 1 or name.endswith('.stop'):
        print('invoking command: {}()'.format(name))
        fcn()
    else:
        print('invoking command: {}({})'.format(name, ms))
        fcn(ms)


if __name__ == '__main__':
    args = sys.argv
    for i in range(1, len(args)):
        arg = args[i]
        arr = arg.split(':')

        cmd_name = arr[0]

        cmd_ms = 0;
        if len(arr) > 1:
            try:
                cmd_ms = int(arr[1])
            except:
                pass

        invoke_command(cmd_name, cmd_ms)

