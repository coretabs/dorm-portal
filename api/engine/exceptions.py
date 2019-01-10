from .utils import i18n


class NoEnoughQuotaException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = i18n.t('lang.errorMessages.reservations.noQuota')
        super().__init__(msg)


class NonFinishedUserReservationsException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = i18n.t('lang.errorMessages.reservations.cantCreateTwoReservations')
        super().__init__(msg)


class NonUpdatableReservationException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = i18n.t('lang.errorMessages.reservations.cantUpdateFinishedReservation')
        super().__init__(msg)


class NonReviewableReservation(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = i18n.t('lang.errorMessages.reservations.cantReviewNonReviewableReservation')
        super().__init__(msg)
