class GoogleCloudProjectApiKeyUnavailableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class GoogleCloudProjectKeyIdUnavailableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class GoogleCloudProjectIdUnavailableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class GoogleCloudServiceAccountEmailUnavailableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
