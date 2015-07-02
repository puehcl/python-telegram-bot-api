# python-telegram-bot-api
A python wrapper and bot builder for the telegram bot api.

Can be found on PyPI https://pypi.python.org/pypi/telegram-bot-api/0.2

## Some simple samples
The simplest way to build a bot with this package is the botbuilder, here are some short and easy ways to create a bot.

### A simple echo bot
```python
import telegram.botapi.botbuilder as botbuilder

  def echo_text(update):
      if len(update.text) >= 7:
        return update.text[6:]
      else:
        return ""
  
  if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="apikey.txt") \
      .send_message_when("echo", echo_text) \
      .build().start()
```
To explain, the `send_message_when` method takes as first argument a command (without the preceding /) and as second
argument a function which acts upon the update which trigged the event (a /echo command) and returns a response message.
Long story short, you send `/echo foobar` to the bot, and it answers with `foobar`.

### A simple photo-bot with a logger
```python
import telegram.botapi.botbuilder as botbuilder

  def logger(update):
    print("received update with text:", update.text)

  def contains_photo(update):
    return "photo" in update.text.lower()
    
  def photo_file_handle(update):
    if "cat" in update.text.lower():
      return open("cat.png", "rb")
    else if "dog" in update.text.lower():
      return open("dog.png", "rb")
    else:
      return open("emu.png", "rb")
      
    if __name__ == "__main__":
      botbuilder.BotBuilder(apikey_file="apikey.txt") \
        .do_when(lambda update: return True, logger, botbuilder.DO_NOT_CONSUME) \
        .send_photo_when("penguin", "penguin.png") \
        .send_photo_when(contains_photo, photo_file_handle) \
        .build().start()
```
In this example, a logger is registered to receive all events via the `do_when` method and a simple lambda which
matches all update events, to allow the event to get passed to other matchers, the `botbuilder.DO_NOT_CONSUME`
constant is used, you can also use `botbuilder.CONSUME` to explicitly state that an update event should be consumed
by the action.

Next, an action is registered, which receives `/penguin` commands and sends back the `penguin.png` file,
the last action is registered to be executed when `contains_photo` matches, that is, if a message contains the the
text "photo", the action then looks for other words specifying the photo to be sent and returns a file handle to it.

| input | output |
| ----- | ------ |
| "/penguin" | contents of the "penguin.png" picture |
| "send me a photo of a cat" | contents of the "cat.png" picture |
| "i want a photo of a dog" | contents of the "dog.png" picture |
| "send me a photo" | contents of the "emu.png" picture |

### Available builder methods

* `do_when(matcher, result_generator, consume=True, optionals={})`
* `send_message_when(matcher, result_generator (or string), consume=True, optionals={})`
* `forward_message_when(matcher, result_generator (or tuple, see below), ...)`
* `send_location_when(matcher, result_generator (or tuple, see below), ...)`
* `send_photo_when(matcher, result_generator (or filename), ...)`
* `send_audio_when(matcher, result_generator (or filename), ...)`
* `send_document_when(matcher, result_generator (or filename), ...)`
* `send_sticker_when(matcher, result_generator (or filename), ...)`
* `send_video_when(matcher, result_generator (or filename), ...)`

Instead of the `result_generator` function, you can instead directly use values as parameters, in the case of
`send_location_when`, you could replace the `result_generator` with a `(latitude, longitude)` tuple.

Optionals are the optional parameters that can be used by the telegram api, in the case of `send_photo_when`,
`{"caption": "A photo of some mountains"}` would be a valid optional parameter. The `result_generator` function
can also return optional parameters as the last item in a tuple or a list, for example
```python
def get_photo(update):
    return open("photo.png", "rb"), {"caption": "some photo"}
```
This can be used if the optional parameters are dependent on the content of the update.

Based on the type of response to send, the `result_generator` has to return different values, this is where it gets
confusing:

* in `do_when`, it can return anything, the value is not used.
* in `send_message_when`, it can return `string`, `string, optionals` or `[string, optionals]`
* in `forward_message_when`, it can return `from_chat_id, message_id[, optionals]` or a list of those items (you get the drift)
* in `send_location_when`, it can return `latitude, longitude[, optionals]` or a list
* in `send_[filetype]_when`, it can return `filehandle_filename_or_id[, is_id][, optionals]`

The `is_id` parameter defaults to `False` and effects the handling of the return value, if it is a string.
If `is_id` is `False`, the returned string will be treated as a filename, if it is `True`, the returned string
will be treated as a file_id for the telegram api. If the returned value is not a string, the `is_id` parameter
is not taken into account.

## Coming Soon

* **connector** explanation
* **bot** explanation
