
get_me_method                   = "getMe"
get_updates_method              = "getUpdates"
get_user_profile_photos_method  = "getUserProfilePhotos"

forward_message_method          = "forwardMessage"
send_message_method             = "sendMessage"
send_photo_method               = "sendPhoto"
send_audio_method               = "sendAudio"
send_document_method            = "sendDocument"
send_sticker_method             = "sendSticker"
send_video_method               = "sendVideo"
send_location_method            = "sendLocation"
send_chat_action_method         = "sendChatAction"

def get_url(base_url, method):
    if base_url[-1] != "/":
        base_url = base_url + "/"
    return base_url + method

def get_me_url(base_url):
    return get_url(base_url, get_me_method)

def get_updates_url(base_url):
    return get_url(base_url, get_updates_method)

def get_user_profile_photos_url(base_url):
    return get_url(base_url, get_user_profile_photos_method)

def forward_message_url(base_url):
    return get_url(base_url, forward_message_method)

def send_message_url(base_url):
    return get_url(base_url, send_message_method)

def send_photo_url(base_url):
    return get_url(base_url, send_photo_method)

def send_audio_url(base_url):
    return get_url(base_url, send_audio_method)

def send_document_url(base_url):
    return get_url(base_url, send_document_method)

def send_sticker_url(base_url):
    return get_url(base_url, send_sticker_method)

def send_video_url(base_url):
    return get_url(base_url, send_video_method)

def send_location_url(base_url):
    return get_url(base_url, send_location_method)

def send_chat_action_url(base_url):
    return get_url(base_url, send_chat_action_method)
