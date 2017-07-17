from hue_api import HueBridge
import math


def compute_hue(value, max_value):
    hue_red = 65535
    hue_green = 25500

    # compute the right parameters needed to convert the given numeric value to the right hue value
    ratio = 1
    if max_value > 0:
        ratio = min(1, value / max_value)
        # compute the current hue
    return int(math.floor(hue_green + (hue_red - hue_green) * ratio))


def set_val(req_hue):
    # the Hue bridge id
    bridge = HueBridge("http://192.168.0.201/api/1jlyVie2nvwtNwl0hv8KdZOO0okdvNcIIdPXWsdX")
    # we want to change the hue value of this lamp
    lamp_id = 1

    try:
                # compute the actual hue
                hue = compute_hue(req_hue, 255.0)
                # debug
                print('Hue: {}'.format(hue))
                # set the hue to the given lamp
                bridge.set_hue(lamp_id, hue)
    except:

        pass