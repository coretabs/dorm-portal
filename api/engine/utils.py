from django.utils.translation import get_language

import i18n as original_i18n


class i18n:
    @staticmethod
    def t(key):
        return original_i18n.t(key, locale=get_language())
