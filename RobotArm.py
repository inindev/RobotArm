#
# RobotArm.py
#
#   copyright 2017 John Clark, apache 2.0 license
#   https://www.apache.org/licenses/LICENSE-2.0
#
#   Python library for OWI Robotic Arm Edge with USB Interface kit
#     Robotic Arm Edge: http://www.owirobot.com/robotic-arm-edge-1
#     USB Interface for Robotic Arm Edge: http://www.owirobot.com/products/USB-Interface-for-Robotic-Arm-Edge.html
#
#   doc used: https://notbrainsurgery.livejournal.com/38622.html
#

#
# udev rule to allow non-root access to arm
# echo ACTION==\"add\", SUBSYSTEM==\"usb\", ATTR{idVendor}==\"1267\" ,ATTR{idProduct}==\"0000\", MODE=\"0666\" | sudo tee -a /etc/udev/rules.d/95-robot.rules
#

import time
import usb.core, usb.util


class DevIO:
    usb_dev = None
    state = [0, 0, 0] # [arm, base, light]
    timeout_ms = 0

    def __init__(self, timeout_ms=250):
        self.timeout_ms = timeout_ms

        self.usb_dev = usb.core.find(idVendor=0x1267, idProduct=0x0000)
        if(self.usb_dev == None):
            raise IOError('failed to connect to robot arm')

        self.stop()

    def send(self, state):
        self.state = state
        self.usb_dev.ctrl_transfer(
            bmRequestType=usb.util.CTRL_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
            bRequest=6,
            wValue=0x100,
            wIndex=0,
            data_or_wLength=self.state,
            timeout=self.timeout_ms)

    def send_merge(self, state):
        new_state = [self.state[0] | state[0], self.state[1] | state[1], self.state[2] | state[2]]
        self.send(new_state)

    def send_remove(self, state):
        new_state = [self.state[0] & ~ state[0], self.state[1] & ~ state[1], self.state[2] & ~ state[2]]
        self.send(new_state)

    def stop(self):
        self.send([0, 0, 0])


class Part:
    def __init__(self, name, dev):
        self.name = name
        self.dev = dev

    def sleep_ms(self, ms):
        time.sleep(ms / 1000.0)

    def add_action(self, name, msg):
        def action(duration_ms=0):
            print('{0}.{1}, msg = {2}, duration = {3} ms'.format(self.name, name, msg, duration_ms))
            self.dev.send_merge(msg)
            if(duration_ms > 0):
                self.sleep_ms(duration_ms)
                stop()
        setattr(self, name, action)

        def stop():
            print('{0}.{1}.stop, msg = {2}'.format(self.name, name, msg))
            self.dev.send_remove(msg)
        setattr(action, 'stop', stop)

        return(self)


class RobotArm:
    dev = DevIO()

    grip = Part('grip', dev)\
        .add_action('close', [1<<0, 0, 0])\
        .add_action('open',  [1<<1, 0, 0])

    wrist = Part('wrist', dev)\
        .add_action('up',    [1<<2, 0, 0])\
        .add_action('down',  [1<<3, 0, 0])

    elbow = Part('elbow', dev)\
        .add_action('up',    [1<<4, 0, 0])\
        .add_action('down',  [1<<5, 0, 0])

    shoulder = Part('shoulder', dev)\
        .add_action('up',    [1<<6, 0, 0])\
        .add_action('down',  [1<<7, 0, 0])

    base = Part('base', dev)\
        .add_action('cw',    [0, 1<<0, 0])\
        .add_action('ccw',   [0, 1<<1, 0])

    light = Part('light', dev) \
        .add_action('off',   [0, 0, 0]) \
        .add_action('on',    [0, 0, 1])
