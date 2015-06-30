
get_updates_method = "getUpdates"

send_message_method = "sendMessage"


def get_url(base_url, method):
    if base_url[-1] != "/":
        base_url = base_url + "/"
    return base_url + method

def get_updates_url(base_url):
    return get_url(base_url, get_updates_method)

def send_message_url(base_url):
    return get_url(base_url, send_message_method)
