
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
        print("new command matcher", self)
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

class StringGenerator(object):
    def __init__(self, obj, optionals={}):
        self.obj = obj
        self.optionals = optionals
        print("new string generator: optionals=", optionals)
    def generate(self, update):
        return str(self.obj)
    def get_optionals(self):
        return self.optionals

class FunctionGenerator(object):
    def __init__(self, function, optionals={}):
        self.function = function
        self.optionals = optionals
        self.base_optionals = optionals
        print("new function generator: optionals=", optionals)
    def generate(self, update):
        print("generator", self, ": optionals=", self.optionals)
        result = self.function(update)
        if result and isinstance(result, (tuple,list)):
            if len(result) == 2:
                result, optionals = result
                self.optionals = self.base_optionals.copy()
                self.optionals.update(optionals)
        return result
    def get_optionals(self):
        return self.optionals

class Action(object):
    def __init__(self, generator):
        self.generator = generator
    def execute(self, update):
        return self.generator.generate(update)

class SendAction(Action):
    def __init__(self, generator, connector):
        super().__init__(generator)
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

class SendFileAction(SendAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector)
        self.is_id = is_id

class SendPhotoAction(SendFileAction):
    def __init__(self, generator, connector, is_id):
        super().__init__(generator, connector, is_id)
        print("new send photo action", self)
    def execute(self, update):
        photo = self.generator.generate(update)
        optionals = self.generator.get_optionals()
        print("generated photo:", photo)
        print("optionals:", optionals)
        kwargs = {"optionals": optionals}
        if isinstance(photo, str):
            if self.is_id:
                kwargs["photo_id"] = photo
            else:
                kwargs["file_or_filename"] = photo
        else:
            kwargs["file_or_filename"] = photo
        return self.connector.send_photo(update.chat.id, **kwargs)
