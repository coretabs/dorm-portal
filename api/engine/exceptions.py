class NoEnoughQuotaException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'No enough quota in this room'
        super().__init__(msg)
