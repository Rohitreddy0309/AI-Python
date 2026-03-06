class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message                          #All other exceptions will inherit from this
        self.status_code = status_code                                          
