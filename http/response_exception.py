class MultipleChoicesError(Exception):
    choices = []

    def __init__(self, choices):
        self.choices = choices


class NotFoundError(Exception):
    def __init__(self):
        pass


class ResponseError(Exception):
    def __init__(self, message):
        self.message = message
