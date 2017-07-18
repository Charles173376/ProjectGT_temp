from hue_api import HueBridge


def set_val(req_bri):

    bridge = HueBridge("http://192.168.0.201/api/6oz5H2zCGHLNuwq-8eDjJqyNCm8ONXOBgS0VOewA")
    lamp_id = 3

    try:

        bridge.set_bri(lamp_id, req_bri)

    except:

        pass


def get_val(datatype):
    bridge = HueBridge("http://192.168.0.201/api/6oz5H2zCGHLNuwq-8eDjJqyNCm8ONXOBgS0VOewA")
    lamp_id = 3

    try:
        return HueBridge.get_bri()

    except:

        pass
