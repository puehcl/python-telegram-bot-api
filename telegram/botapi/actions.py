
class UpdateMatcher(object):
    def matches(self, update):
        pass

class FunctionMatcher(UpdateMatcher):
    def __init__(self, function):
        self.function = function
    def matches(self, update):
        return self.function(update)

class CommandMatcher(UpdateMatcher):
    def __init__(self, commandstr):
        self.commandstr = str(commandstr)
    def matches(self, update):
        if update.text:
            return update.text.lower().startswith("/" + self.commandstr)
        return False

class Generator(object):
    def generate(self, update):
        pass
    def get_optionals(self):
        return {}

class StringGenerator(Generator):
    def __init__(self, obj, optionals={}):
        self.obj = obj
        self.optionals = optionals
    def generate(self, update):
        return str(self.obj)
    def get_optionals(self):
        return self.optionals

class TupleGenerator(Generator):
    def __init__(self, tup, optionals={}):
        self.tuple = tup
        self.optionals = optionals
    def generate(self, update):
        return self.tuple
    def get_optionals(self):
        return self.optionals

class FunctionGenerator(Generator):
    def __init__(self, function, optionals={}):
        self.function = function
        self.optionals = optionals
        self.base_optionals = optionals
    def generate(self, update):
        result = self.function(update)
        if result and isinstance(result, (tuple,list)):
            if len(result) >= 2:
                if isinstance(result[-1], dict):
                    optionals = result[-1]
                    result = result[:-1]
                    self.optionals = self.base_optionals.copy()
                    self.optionals.update(optionals)
        return result
    def get_optionals(self):
        return self.optionals

class Action(object):
    def __init__(self, function):
        self.function = function
    def execute(self, update):
        return self.function(update)

class SendAction(Action):
    def __init__(self, generator, connector):
        self.generator = generator
        self.connector = connector
    def execute(self, update):
        return None

class SendMessageAction(SendAction):
    def __init__(self, generator, connector):
        super().__init__(generator, connector)
    def execute(self, update):
        message = self.generator.generate(update)
        optionals = self.generator.get_optionals()
        return self.connector.send_message( update.chat.id, \
                                            message, \
                                            optionals=optionals)

class ForwardMessageAction(SendAction):
    def __init__(self, generator, connector):
        super().__init__(generator, connector)
    def execute(self, update):
        from_chat_id, message_id = self.generator.generate(update)
        optionals = self.generator.get_optionals()
        return self.connector.forward_message(  update.chat.id, \
                                                from_chat_id, \
                                                message_id, \
                                                optionals=optionals)

class SendFileAction(SendAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector)
        self.is_id = is_id
    def _get_kwargs(self, update, type_name):
        file_filename_or_id = self.generator.generate(update)
        if isinstance(file_filename_or_id, (tuple,list)):
            if len(file_filename_or_id) == 2:
                file_filename_or_id, is_id = file_filename_or_id
                self.is_id = self.is_id or is_id
        optionals = self.generator.get_optionals()
        kwargs = {"optionals": optionals}
        if isinstance(file_filename_or_id, str):
            if self.is_id:
                kwargs["{}_id".format(type_name)] = file_filename_or_id
            else:
                kwargs["file_or_filename"] = file_filename_or_id
        else:
            kwargs["file_or_filename"] = file_filename_or_id
        return kwargs

class SendPhotoAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
    def execute(self, update):
        kwargs = self._get_kwargs(update, "photo")
        return self.connector.send_photo(update.chat.id, **kwargs)

class SendAudioAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
    def execute(self, update):
        kwargs = self._get_kwargs(update, "audio")
        return self.connector.send_audio(update.chat.id, **kwargs)

class SendDocumentAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
    def execute(self, update):
        kwargs = self._get_kwargs(update, "document")
        print("sending documents with", kwargs)
        return self.connector.send_document(update.chat.id, **kwargs)

class SendStickerAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
    def execute(self, update):
        kwargs = self._get_kwargs(update, "sticker")
        return self.connector.send_sticker(update.chat.id, **kwargs)

class SendVideoAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
    def execute(self, update):
        kwargs = self._get_kwargs(update, "video")
        return self.connector.send_video(update.chat.id, **kwargs)

class SendLocationAction(SendAction):
    def __init__(self, generator, connector):
        super().__init__(generator, connector)
    def execute(self, update):
        latitude, longitude = self.generator.generate(update)
        optionals = self.generator.get_optionals()
        return self.connector.send_location(update.chat.id, \
                                            latitude, longitude, \
                                            optionals)
