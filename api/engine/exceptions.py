class NoEnoughQuotaException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'No enough quota in this room'
        super().__init__(msg)


class NonFinishedUserReservationsException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'You cannot create a reservation till you finish the previous one'
        super().__init__(msg)


class NonUpdatableReservationException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = 'You cannot update this reservation, please create another one'
        super().__init__(msg)
