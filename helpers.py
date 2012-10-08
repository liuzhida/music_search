#import simplejson as json
import json
import time

def json_encode(dict_data):
    if not dict_data:
        return json.dumps('')
    try:
        return json.dumps(dict_data, default=_json_handler)
    except:
        raise ValueError

def _json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return None

json_decode = json.loads

def ctime():
    return time.strftime('%F %R',time.localtime(time.time()))
