import __conf__
import controller_traffic
import math


def get_speed(r, filter):
    if r == 0:
        return controller_traffic.get_speed_limit()

    # v = math.e ** r * __conf__,ar_factor

    v = math.sqrt(__conf__.ar_max * abs(r))

    v = min(v, controller_traffic.get_speed_limit())

    # max_speed = controller_traffic.get_speed_limit()
    # if r == 0:
    #    speed = max_speed
    # else:
    #    speed = max_speed * abs(r) * 0.3

    # v = filter.get([min(math.sqrt(speed), max_speed)])
    return v
