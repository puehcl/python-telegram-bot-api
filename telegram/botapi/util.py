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

    def __repr__(self):
        return self.__str__()


def fromjson(json_dict):
    return JsonObject(json_dict)

def iscallable(obj):
    return hasattr(obj, "__call__")

def getfile(file_or_filename):
    if file_or_filename:
        if isinstance(file_or_filename, str):
            return open(file_or_filename, "rb")
        else:
            return file_or_filename
    else:
        return None

def getparam(name, file_id):
    if file_id:
        return {name: file_id}
    else:
        return {}

def getmultipart(name, fil):
    if fil:
        return {name: fil}
    else:
        return {}
