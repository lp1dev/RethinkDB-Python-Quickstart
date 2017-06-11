class ThinkTwiceException(Exception):
    def __init__(self, message, code):
        super(ThinkTwiceException, self).__init__(message)
        self.message = message
        self.code = code
