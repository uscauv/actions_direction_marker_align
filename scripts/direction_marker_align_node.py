#!/usr/bin/env python

import rospy

import actionlib

from vision_common.msg import Targets
from direction_marker_align.msg import AlignAction


class DirectionMarkerAlignNode():
    enabled = True

    def __init__(self):
        rospy.init_node('direction_marker_align')

        rospy.Subscriber('/vision/direction_marker/targets', Targets, self.on_targets)

        self._as = actionlib.SimpleActionServer(rospy.get_name(), AlignAction,
                                                execute_cb=self.on_action, auto_start=False)
        self._as.start()

    def on_action(self, action):
        rospy.loginfo('got action goal, enabling')
        self.enabled = True

    def on_targets(self, targets):
        if self.enabled:
            rospy.loginfo('got target messages, acting on it')

            # TODO: we probably want to do something more intelligent here, but for now let's just pick the first one
            target = targets.targets[0]

            # now we can use a simple PID controller to move the sub to be centered over the marker.
            max_x_speed = rospy.get_param('/action/direction_marker_align/max_x_speed', 0.4)
            max_y_speed = rospy.get_param('/action/direction_marker_align/max_y_speed', 0.4)
            max_twist_speed = rospy.get_param('/action/direction_marker_align/max_twist_speed', 0.4)

            x_speed = max_x_speed * target.x
            y_speed = max_y_speed * target.y
            twist_speed = max_twist_speed * (target.angle - 90)  # 90 degrees is straight-up-and-down

            print(x_speed, y_speed, twist_speed)


if __name__ == '__main__':
    node = DirectionMarkerAlignNode()
    rospy.loginfo('created')
    rospy.spin()