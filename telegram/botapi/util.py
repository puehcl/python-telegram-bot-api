import json

class JsonObject(object):

    def __init__(self, json_data):
        self.__dict__ = dict()
        for key in json_data:
            value = json_data[key]
            if isinstance(value, dict):
                value = JsonObject(value)
            if isinstance(value, list):
                values = []
                for item in value:
                    values.append(JsonObject(item))
                value = values
            self.__dict__[key] = value

    def __getattr__(self, attr):
        if not attr in self.__dict__:
            return None
        return self.__dict__[attr]

    def __str__(self):
        result = "JsonObject{"
        for key in self.__dict__:
            result = result + str(key) + ":" + str(self.__dict__[key]) + ", "
        result = result[:-2] + "}"
        return result


def fromjson(string):
    return JsonObject(json.loads(string))

def iscallable(obj):
    return hasattr(obj, "__call__")
    
