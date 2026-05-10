class PixelsDiceNameIsMissingException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class PixelsDiceRequestQueueException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
